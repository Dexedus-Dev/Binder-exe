# Hello, I'm EQ.

I created a program called **Binder** that combines multiple executable files into one.  
I'm not very fluent in English — most of this was written using Google Translate.  
If you have any questions or if something is unclear, please feel free to [email me](mailto:dexedusd@gmail.com).

## Workflow Diagram – EXE Binder

```mermaid
graph TD
    A[Start] --> B[User inputs EXE File One and Two or via command-line arguments]
    B --> C[embed_files.py reads EXE files as bytes]
    C --> D[Generates embedded dictionary in loader.py]
    D --> E[loader.py writes EXEs to temporary files]
    E --> F[Each EXE is executed using threading and subprocess]
    F --> G[main.py optionally compiles loader.py into a single EXE using Nuitka]
    G --> H[Output: A single EXE that runs both original programs]
    H --> I[Done]
