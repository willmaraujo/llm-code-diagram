Great. I will extract only the essential flowchart syntax information from the Mermaid documentation you linked, excluding any website navigation or unrelated text. I’ll retain the relevant syntax, descriptions, and examples, and structure the output clearly for easy model fine-tuning.
I’ll let you know once it’s ready for your review.

Mermaid Flowchart Syntax

Mermaid flowcharts are defined using a text-based syntax. Below is a comprehensive summary of the keywords, operators, and syntax for Mermaid flowcharts, including node definitions, shapes, link types, subgraphs, and other key features. Example code snippets are provided for clarity.

Flowchart Declaration and Direction

Graph keyword: Begin a flowchart with the keyword flowchart (or the alias graph) followed by a direction indicator. For example:

flowchart LR
Start --> Stop

Direction indicators: Possible flowchart orientations are:

TB – Top to Bottom

TD – Top Down (same as top to bottom)

BT – Bottom to Top

RL – Right to Left

LR – Left to Right

Example: flowchart TD defines a top-down diagram, whereas flowchart LR defines a left-to-right diagram.

Semicolons: Ending statements with ; is optional. The below are equivalent:

flowchart LR
A-->B;
B-->C

flowchart LR
A --> B
B --> C

Spacing: A single space is allowed between node identifiers and the link operator for readability (e.g. A --> B instead of A-->B), but do not put spaces between a node identifier and its label text or between a link operator and its link text.

Warning: Do not use the lowercase word end by itself as a node ID, as it conflicts with the subgraph syntax. Use capitalization (e.g. End, END) or another workaround. Also avoid starting an edge with a node id that is just o or x in lowercase without a space, as these letters are used for special link markers (prefix with a space or uppercase them if needed).

Node Syntax and Shapes

Flowchart nodes are declared by an identifier followed by optional text or shape notation. The identifier (ID) is shown inside the node by default. You can specify a custom label or change the node shape using special characters around the label text.

Basic Node and Label

Default node: Simply writing an ID creates a node (displaying the ID as its text). For example, id1 alone will produce a default node (a rectangle) labeled “id1”.

Node with label: Use square brackets [...] to specify a label different from the ID. For example:

flowchart LR
id1[This is the text in the box]

This defines a node with ID id1 but displayed text “This is the text in the box”. If you redefine the label for the same node ID later, the last label is used.

Unicode text: You can include Unicode characters in labels by enclosing the text in quotes "[文字]".

Markdown in labels: (Mermaid v10+) Nodes (and edge labels) support basic Markdown for bold and italic text. Use double quotes and backticks for complex formatting. For example, "**bold** _italic_" in a label will render formatted text. Mermaid also auto-wraps long text and supports line breaks with actual newline characters (instead of <br> tags). This behavior (automatic wrapping) can be disabled via configuration (markdownAutoWrap: false).

Standard Shape Notation (Legacy)

By using specific wrapping characters around the node text, you can change the shape of the node. The following shapes are available using the legacy notation:

Rectangle (default): Use [Text] or no special wrapper. Example: A[Rectangle] yields a rectangular node.

Rounded rectangle: Use parentheses (...). Example:

flowchart LR
A(Rounded corners)

This creates a node with rounded edges.

Stadium shape: Use ( [ ] ) – an outer parenthesis and inner brackets. Example: A([Stadium]).

Subroutine shape: Use double brackets [[...]]. Example: A[[Subroutine]].

Cylinder (database): Use [(...)] – brackets inside parentheses. Example: A[(Database)].

Circle: Use double parentheses ((...)). Example: A((Circle)).

Asymmetric shape: Use > ... ] – greater-than and a closing bracket. Example: A>Asymmetric] (an asymmetric trapezoid shape).

Rhombus (diamond): Use curly braces {...}. Example: A{Diamond}.

Hexagon: Use double curly braces {{...}}. Example: A{{Hexagon}}.

Parallelogram (lean-right): Use /.../ inside brackets. Example: A[/Parallel/].

Parallelogram (lean-left): Use \...\ inside brackets. Example: A[\\Parallel\\].

Trapezoid: Use / at the start and \ at the end inside brackets. Example: A[/Trapezoid\].

Trapezoid (alt): Use \ at the start and / at the end inside brackets. Example: B[\Trapezoid/].

Double Circle: Use triple parentheses (((...))) for a double-ring circle. Example: A(((Double Circle))).

Note: The asymmetric shape using >...] currently only works in one orientation (it does not have a mirrored version).

Extended Shape Syntax (Mermaid v11.3+)

Mermaid 11.3 introduced a generalized syntax to support many more node shapes. You can assign a shape by using the @{ ... } notation after the node ID. For example:

flowchart LR
A@{shape: rect}

This defines node A as a rectangle (equivalent to A["A"] or just A). You can specify any supported shape name in place of rect.

New shape names (v11.3+): Mermaid supports ~30 shape keywords. Some examples include:

rect (Rectangle – default process)

stadium (Stadium – terminal point)

subroutine (Framed rectangle – subprocess)

cyl (Cylinder – database/storage)

circle (Circle – start/end)

dbl-circ (Double Circle – end/stop)

diamond (Decision diamond – alias for diam)

hex (Hexagon – preparation step)

parallelogram / parallelogram alt (Sloped rectangles) – use sl-rect or trap-b etc.

notch-rect (Notched rectangle – card)

hourglass (Hourglass shape – collate)

bolt (Lightning bolt shape – communication link)

brace / brace-r / braces (Curly brace shapes – comment indicators)

lean-right / lean-left (Lean parallelograms – input/output)

fork (Fork/Join bar – thick horizontal/vertical line)

tri (Triangle – extract)

flag (Flag/Paper tape)

odd (Odd shape)

(This is not the full list, but a selection of shape keywords. See Mermaid docs for the complete list.) Each shape keyword can be used in the shape: field of the @{} syntax. Many shapes also have alias names (e.g., database or db as aliases for the cylinder shape).

Icon and Image Nodes (v11.3+)

Mermaid v11.3 added special shapes for icons and images:

Icon shape: Use shape: 'icon' with parameters for icon name and styling. For example:

flowchart LR
node1@{shape: 'icon', icon: 'face-smile', form: 'circle', label: 'User', pos: 'b'}

Here icon: 'face-smile' is the icon (from a pre-registered icon pack), form: 'circle' adds a circular background, label: 'User' adds text, and pos: 'b' positions the label at the bottom. (Icon backgrounds can be square, circle, rounded, or none; label position can be top t or bottom b.)

Image shape: Use shape: 'image' with parameters for the image URL and optional properties. For example:

flowchart LR
pic1@{shape: 'image', img: 'https://example.com/pic.png', label: 'Picture', pos: 't', w: 100, h: 100}

This displays an image from the URL with a label “Picture” above it. You can specify width w and height h (in pixels); if not specified, the image’s natural size is used. The constraint: 'on' option can be used to constrain node size to the image aspect ratio.

(Ensure you register any required icon packs before using icon shapes. Image and Icon shapes may not render in all environments if external resources are restricted.)

Links (Edges) Between Nodes

Nodes are connected by edges (links) using arrow notation. By default, an arrow is drawn from one node to another. Links can have different styles and can include labels.

Basic Link Types

Arrow (directed link): Use --> to draw an arrow from one node to another. For example:

A-->B

This produces an arrow pointing from A to B (arrowhead at B).

Open link (undirected line): Use three hyphens --- to draw a line with no arrowheads. Example: A --- B connects A and B with a plain line.

Both ends arrow: Use <--> to draw arrows on both ends of the line (bi-directional link).

No arrow (invisible): In some cases, an “invisible” link can be used (e.g. for spacing). Mermaid uses an open link with no markers for this purpose (same syntax as an open link).

Text Labels on Links

You can attach text labels to links in two ways:

Inline text: Place the text between two hyphen sets. For example:

A-- This is the text! ---B

or with an arrow:

A-- text -->B

In the first form, the text is included between the link lines (works well for long phrases). In the second form, the text before the arrow is associated with the link.

Using the | separator: Enclose the text in | on the arrow. For example:

A---|This is the text|B

or for an arrow:

A-->|text|B

```.
This explicitly separates the link label from the arrow syntax.

Both methods result in “A — text —> B” style labeled arrows. The choice is mostly stylistic; using |text| can be clearer for arrows.

Link Style Variations

Dotted link: Use -.-> for a dashed/dotted line arrow. For example: A-.->B produces a dotted line with an arrow at B.

Dotted link with text: Combine the syntax:

A-. text .-> B

This creates a dotted line from A to B with “text” centered on it.

Thick link: Use ==> for a thick (bold) line arrow. E.g. A ==> B yields a thick arrow from A to B.

Thick link with text: For example:

A == label ==> B

creates a thick arrow with “label” on it.

Cross-head or Circle-head arrows: Mermaid supports special terminators:

--o adds a circle terminator. E.g. A--o B draws an arrow from A to B with a hollow circle at B. o-- would put a circle at the tail (A).

--x adds a cross (X) terminator. E.g. B --x C draws an arrow from B to C with a cross at C. x-- puts a cross at the start.

Multi-directional arrows: You can put terminators on both ends or use two-headed arrows:

A o--o B (circle at both ends).

B <--> C (arrowheads at both ends).

C x--x D (cross at both ends).

Chaining and Merging Links

Mermaid allows shorthand for multiple links in one line:

Chain multiple links sequentially: Use a series of --> in one statement. For example:

A -- text --> B -- text2 --> C

This creates A→B and B→C with labels in one line.

Split one source to multiple targets: Use the & separator. For example:

a --> b & c --> d

This creates links a→b and c→d in one line (two separate chains split by &).

Multiple sources to multiple targets: You can chain both sides with &. For example:

A & B --> C & D

This produces links A→C, A→D, B→C, B→D all in one line (a combination of two sources and two targets).

Note: While chaining is powerful, overusing it can make the code harder to read. Use it judiciously.

Controlling Link Length (Rank Spacing)

By default, the automatic layout determines the distance (rank separation) of nodes. You can extend the length of a link by adding extra hyphens (or dots/equals for dotted/thick) in the link operator.

Each extra - adds one more rank distance. For example, compare:

B --> E (normal length) vs. B ----> E (with two extra dashes). The second will force E to be placed further away from B (two additional ranks apart).

If a link has a label in the middle (using the -- text --> style), put the extra dashes on the right side of the label. For example:

B -- No ----> E

ensures the extra length is applied despite the label.

For dotted or thick links, use extra . or = respectively to extend length. For example, B -...-> E (dotted) or B ====> E (thick) for a longer link.

The table below (from Mermaid docs) summarizes the patterns:

Normal: --- (1 rank), ---- (2 ranks), ----- (3 ranks)

Normal w/ arrow: -->, --->, ----> (increasing ranks)

Thick: ===, ====, =====

Thick w/ arrow: ==>, ===>, ====>

Dotted: -.-, -..-, -...-

Dotted w/ arrow: -.->, -..->, -...->

Note: The layout engine might still increase link lengths beyond what you request, to accommodate other diagram constraints.

Edge IDs and Animations (Advanced)

Assigning IDs to edges: You can give an edge its own ID (name) by prefixing the link with id@. For example:

flowchart LR
    A e1@--> B

Here e1 is the identifier for the A→B link. This allows referencing that specific edge later (for styling, etc.).

Using edge IDs: Once an edge has an ID, you can target it in style or class definitions similar to nodes. For instance, Mermaid supports defining classes and applying them to edges by ID:

Define a class with classDef, including animation or style properties.

Apply it to the edge using class <edgeId> <className>.Example:

flowchart LR
    A e1@--> B
    classDef animate stroke-dasharray: 5 5, animate:true, color:red;
    class e1 animate

In this snippet, e1@--> creates an edge with ID “e1”. Then a class named animate is defined (with a dashed line and animation enabled), and that class is applied to edge e1. This would make the edge animated (blinking/red/dashed, depending on the style).

Built-in animation shorthand: Mermaid (v10+) provides a shorthand to turn on edge animation by specifying an animation speed:

e.g., an edge marked as {animation: 'fast'} is equivalent to animate: true with fast speed. (This can be set via directives or class definitions as shown above.)

(Edge animations and styling require Mermaid configurations that allow them, and might not be enabled by default in all integrations.)

Special Characters and Escaping

Certain characters can interfere with the Markdown/mermaid syntax. To include them in labels:

Quoted labels: Enclose the label in quotes "[text]" to include special characters like commas, parentheses, etc., without breaking the syntax. For example:

id1["This is the (text) in the box"]

This allows parentheses in the label text.

HTML entities: You can use HTML entity codes to escape characters. For example, " can be written as #quot; and will render as a double quote. Similarly, #9829; would render as a ♥ symbol. Unicode numeric codes are interpreted in base 10, and named HTML entities (like &amp;) are also supported.

Using these methods, you can include symbols or reserved characters in node labels or link labels safely.

Subgraphs

A subgraph groups nodes and links inside a labeled box. The syntax is:

subgraph [subgraph_id] Subgraph Title
    ... (nodes and links) ...
end

The subgraph_id is optional; if provided, it assigns an internal ID to the subgraph (allowing linking to it). If not given, the title text itself serves as the identifier for linking purposes.

Example:

flowchart TB
    subgraph one
        A1-->A2
    end
    subgraph two
        B1-->B2
    end
    one --> two

This defines two subgraphs “one” and “two”, each with two nodes and a link, then connects subgraph one to subgraph two.

Edges to/from subgraphs: You can treat a subgraph like a node when linking. In the example above, one --> two connects the two subgraphs. You can also connect a node to a subgraph, or vice versa, using the subgraph’s ID or title.

Direction within subgraphs: You can override the layout direction inside a subgraph by adding a direction LR, TB, etc., line as the first element in that subgraph. For example:

flowchart LR
  subgraph group1
    direction TB
    X --> Y
  end
  A --> B & A --> X

Here, nodes X and Y inside group1 will flow top-to-bottom, even though the overall diagram is left-to-right.

Subgraph title: The text after the (optional) ID in the subgraph line is used as the title label on the subgraph’s container.

Closing: Every subgraph block must end with the keyword end on its own line.

Limitation: If any node inside a subgraph is connected to a node outside the subgraph, then the subgraph’s internal direction setting will be ignored; the subgraph will inherit the parent graph’s direction. Essentially, external links force the subgraph to align with the global layout.

(Remember: the identifier end is reserved for closing subgraphs, so avoid using “end” as a node ID in your flowcharts.)

Interaction (Clickable Nodes)

You can make nodes interactive by binding a click event or link to them:

Use the click keyword followed by a node ID and a callback or URL. Syntax:

click <nodeId> <functionName or "URL"> ["Tooltip text"]

Example usage for a callback function:

flowchart LR
    A-->B
    click A callback

This will call a JavaScript function named callback when node A is clicked. If you want to call a function immediately, use call functionName().

You can also provide a URL in quotes to open when the node is clicked (this opens in a new tab). For example:

click B "https://example.com" "Go to example site"

would make node B a link to a webpage with a tooltip on hover.

The tooltip text is optional and is given in the second quoted string (as shown above). If provided, it appears when hovering over the node.

Note: Interaction features might be disabled in certain security modes. For instance, if securityLevel is set to strict in Mermaid config, the click functionality is turned off (it’s enabled in loose mode). Also, the actual callback function must be defined in the environment where the graph is embedded (in the web page’s script).
```
