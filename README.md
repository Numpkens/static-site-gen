# Static Website Generator

This is a python program that generates a static website.

## Description

This project is a foundational static-site generator written in Python, designed to function as a clear, modular application demonstrating core backend competencies. The main technical challenge was designing an efficient parsing pipeline that handles the conversion of unstructured Markdown input into a structured HTML output. The implementation demonstrates robust file system traversal (I/O operations) and a clear separation between the data models (TextNode) and the presentation layer (HTMLNode), a core principle for scalable API and microservices design.


🧠 Rationale & Architectural Design

The architecture was designed to enforce separation of concerns—a critical practice for back-end scalability and testability:

    Parsing & I/O Isolation: The conversion logic (text_node_to_html_node) is deliberately isolated from the core data structures and HTML rendering. This ensures the I/O component can be cleanly replaced or optimized (e.g., swapping Python's file handlers for Go's concurrent I/O with Goroutines in a future iteration).

    Testability: The core logic is built around unit tests for every function (test_split_nodes_delimiter), confirming the application's ability to maintain high data integrity as new features are introduced.

    Design Pattern: The use of ParentNode and LeafNode implements a basic Composite Pattern, which is essential for managing hierarchical data structures—a skill directly transferable to designing complex REST API payloads.

## Getting Started

```bash
git clone [https://github.com/Numpkens/static-site-gen.git(https://github.com/Numpkens/static-site-gen.git])
cd static-site-gen
```
## Usage

Running the Main Script

To run the main program, use the provided main.sh shell script from the project root:
Bash

./main.sh

Running the Tests

To run the unit tests and verify the code's functionality, use the test.sh script:
Bash

./test.sh

📂 File Structure

/your-project-root/
├── .gitignore
├── main.sh
├── test.sh
└── src/
    ├── __init__.py
    ├── main.py
    ├── textnode.py
    └── htmlnode.py


🤝 Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, please open an issue or submit a pull request.

✍️ Author

    David Gagnon - Numpkens

## Daily Log

9/22/25 Today I set up the initial file sturcture of the project. 

9/23/2025 I created a shell script to run the main.py file. Then moved on to setting up the main files for the project:
    - textnode.py: This is the foundational file that defines the textnode class and the texttype enum. I made the TextNode a data structure that represents a piece of text with a specific style. The TextType enum provides a way to catergorize these different styles.  In the is file I also put a split nodes delimiter which helps parse the Markdown syntax.
        - htmlnode: Contains the classes that will be used to generate HTML these classes include:
            -HTMLNode: The base class for all html elements.
            -LeafNode: This is are simple HTML tags that dont have any children.
            -ParentNode: A more complex class that represents HTML tags that do have children.
        - text_node_to_html_node: this is the miost importaant function so far. It converts a TextNode into an HTMLNode so that it can be rendered as HTML.
Side note(as of right the main.py file is set up to demonstrate a simple use of a TextNode. It creates a link node and prints it to the console.)

The most challenging today were the test files and this is where i ran into the most issues. The intent is that each test file is dedicated to ensuring that each function executes as expected. The four tests that have been created so far are:
1. test_textnode.py: Checks the functionality of the TextNode class, particularly its equality checks (__eq__) to ensure two nodes with the same properties are considered identical.

2. test_htmlnode.py: Validates the HTML generation from the HTMLNode classes, including the correct rendering of properties, leaf nodes, and parent nodes with children.

3. test_textnode_to_htmlnode.py: Focuses on the conversion process from a TextNode to an HTMLNode, ensuring that each type of TextNode is correctly mapped to its corresponding HTML tag.

4. test_split_nodes_delimiter.py: We just created this file to specifically test the new split_nodes_delimiter function, making sure it handles various delimiters and edge cases correctly.

Challenges I faced today were:
1. I had a name error in the text node to html node function because I forgot to import from textnode.py 
2. I had an attribute error because of a name inconsistentacy.  I am finding as the project grows the name it becoming increasingly difficult and it is easy to get "lost" in the code. 
3. Had a ValueError in the conversion function because I had not yet equuiped it with being able to handle TextType.LINK.  I handled this by inserting an if statement to the function to handle the LINK nodes and to create an <a> HTML tag. 
4. I also had a test case mismatch. This one was harder to find becuase it had to do with the testing of the code.  The test case was excepting an incorrect number of nodes. The function produced 5 nodes but the test asserted 4. I corrected this by updating the test in my code to expect 5 instead of 4. This proved the function was working correctly.



📄 License

This project is licensed under the MIT License - see the LICENSE.md file for details.
