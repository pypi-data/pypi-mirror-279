from dataclasses import dataclass
import os
from typing import Union
from rich.style import Style
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.message import Message
from textual.reactive import Reactive, reactive
from textual.widgets import Static, Tree
from textual.widgets.tree import TreeNode

from posting.collection import Collection, RequestModel
from posting.widgets.collection.new_request_modal import (
    NewRequestData,
    NewRequestModal,
)


TOGGLE_STYLE = Style.from_meta({"toggle": True}) + Style(dim=True)
SUFFIX = ".posting.yaml"


CollectionNode = Union[Collection, RequestModel]


class CollectionTree(Tree[CollectionNode]):
    BINDINGS = [
        Binding("k", "cursor_up", "Cursor Up", show=False),
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("enter,l,h", "select_cursor", "Select Cursor", show=False),
        Binding("space,r", "toggle_node", "Toggle Expand", show=False),
        Binding("n", "new_request", "New Request"),
    ]

    COMPONENT_CLASSES = {
        "node-selected",
    }

    DEFAULT_CSS = """\
    CollectionTree { 
        & .node-selected {
            background: $primary-lighten-1;
            color: $text;
            text-style: bold;
        }
    }
    
    """

    @dataclass
    class RequestSelected(Message):
        request: RequestModel
        node: TreeNode[CollectionNode]
        tree: "CollectionTree"

        @property
        def control(self) -> "CollectionTree":
            return self.tree

    currently_open: Reactive[TreeNode[CollectionNode] | None] = reactive(None)

    def watch_currently_open(self, node: TreeNode[CollectionNode] | None) -> None:
        if node and isinstance(node.data, RequestModel):
            self.post_message(
                self.RequestSelected(
                    request=node.data,
                    node=node,
                    tree=self,
                )
            )

    def render_label(
        self, node: TreeNode[CollectionNode], base_style: Style, style: Style
    ) -> Text:
        """Render a label for the given node.

        Args:
            node: A tree node.
            base_style: The base style of the widget.
            style: The additional style for the label.

        Returns:
            A Rich Text object containing the label.
        """
        # If the tree isn't mounted yet we can't use component classes to stylize
        # the label fully, so we return early.

        node_label = node._label.copy()
        if node_label.plain.endswith(SUFFIX):
            node_label = Text(node_label.plain[: -len(SUFFIX)], style=node_label.style)

        if not self.is_mounted:
            return node_label

        if node._allow_expand:
            prefix = (
                "▼ " if node.is_expanded else "▶ ",
                base_style + TOGGLE_STYLE,
            )
            node_label.append("/")
            node_label.stylize(Style(dim=True, bold=True))
        else:
            method = (
                f"{'█ ' if node is self.currently_open else ' '}{node.data.method[:3]} "
                if isinstance(node.data, RequestModel)
                else ""
            )
            node_label = Text.assemble((method, Style(dim=True)), node_label)
            prefix = ""

        node_label.stylize(style)

        if node is self.currently_open:
            open_style = self.get_component_rich_style("node-selected")
        else:
            open_style = ""

        text = Text.assemble(
            prefix,
            node_label,
            style=open_style,
        )
        return text

    @on(Tree.NodeSelected)
    def on_node_selected(self, event: Tree.NodeSelected[CollectionNode]) -> None:
        event.stop()
        if isinstance(event.node.data, RequestModel):
            self.currently_open = event.node
            self._clear_line_cache()
            self.refresh()

    async def action_new_request(self) -> None:
        # Get the current highlighted node.
        cursor_node = self.cursor_node
        if cursor_node is None:
            # If it's None, we'll add a new RequestModel to the root of the tree.
            target = self.root
        else:
            node_data = cursor_node.data
            if isinstance(node_data, Collection):
                # If it's a Collection, we'll add a leaf to it directly.
                target = cursor_node
            elif isinstance(node_data, RequestModel):
                # If it's a RequestModel, we'll add a new RequestModel to it's parent Collection.
                target = cursor_node.parent or self.root
            else:
                target = self.root

        data = target.data
        assert data is not None, "all nodes should have data"

        def _handle_new_request_data(new_request_data: NewRequestData | None) -> None:
            """Get the new request data from the modal, and update the UI with it."""
            if new_request_data is None:
                # Happens when the user presses `escape` while in the modal.
                return

            # The user confirms the details in the modal, so use these details
            # to create a new RequestModel and add it to the tree.
            request_name = new_request_data.title
            file_name = new_request_data.file_name
            new_request = RequestModel(
                name=request_name, path=data.path / f"{file_name}"
            )
            new_node = target.add_leaf(request_name, data=new_request)
            self.currently_open = new_node
            self.call_later(self.select_node, new_node)

        await self.app.push_screen(NewRequestModal(), callback=_handle_new_request_data)


class RequestPreview(VerticalScroll):
    DEFAULT_CSS = """\
        RequestPreview {
            height: auto;
            max-height: 50%;
            padding: 0 1;
            dock: bottom;
            background: transparent;
            border-top: solid $accent 35%;
            &.hidden {
                display: none;
            }
        }
    """

    request: Reactive[RequestModel | None] = reactive(None)

    def compose(self) -> ComposeResult:
        self.can_focus = False
        yield Static("", id="description")

    def watch_request(self, request: RequestModel | None) -> None:
        self.set_class(request is None, "hidden")
        if request:
            description = self.query_one("#description", Static)
            description.update(request.description)


class CollectionBrowser(Vertical):
    DEFAULT_CSS = """\
    CollectionBrowser {
        height: 1fr;
        dock: left;
        width: auto;
        max-width: 33%;
        & Tree {
            min-width: 20;
            background: transparent;
        }
    }
    """

    def __init__(
        self,
        collection: Collection | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.collection = collection

    def compose(self) -> ComposeResult:
        self.border_title = "Collection"
        self.add_class("section")
        collection = self.collection
        if collection is None:
            return

        tree = CollectionTree(
            label=collection.name,
            data=collection,
            id="collection-tree",
        )
        tree.guide_depth = 1
        tree.show_root = False
        tree.show_guides = False
        self.border_subtitle = collection.name

        def add_collection_to_tree(
            parent_node: TreeNode[CollectionNode], collection: Collection
        ) -> None:
            # Add the requests (leaf nodes)
            for request in collection.requests:
                parent_node.add_leaf(request.name, data=request)

            # Add the subcollections (child nodes)
            for child_collection in collection.children:
                child_node = parent_node.add(
                    child_collection.name, data=child_collection
                )
                add_collection_to_tree(child_node, child_collection)

        # Start building the tree from the root node
        add_collection_to_tree(tree.root, collection)

        tree.root.expand_all()
        yield tree
        yield RequestPreview()

    @on(CollectionTree.RequestSelected)
    def on_request_selected(self, event: CollectionTree.RequestSelected) -> None:
        if isinstance(event.node.data, RequestModel):
            self.request_preview.request = event.node.data

    @on(Tree.NodeHighlighted)
    def on_node_highlighted(self, event: Tree.NodeHighlighted[CollectionNode]) -> None:
        node_data = event.node.data
        # TODO - display more preview data.
        #  It's already all in the node, just need to display it.
        if isinstance(node_data, RequestModel):
            self.request_preview.request = node_data
        else:
            self.request_preview.request = None

    @property
    def request_preview(self) -> RequestPreview:
        return self.query_one(RequestPreview)
