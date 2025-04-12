# Hello, I'm EQ.

I created a program called **Binder** that combines multiple executable files into one.  
I'm not very fluent in English — most of this was written using Google Translate.  
If you have any questions or if something is unclear, please feel free to [email me](mailto:dexedusd@gmail.com).

## Workflow Diagram – EXE Binder

```mermaid
graph TD
    A[Start] --> B[User Inputs EXE File One and Two or via args]
    B --> C[embed_files.py reads EXE files as bytes]
    C --> D[Generate embedded dict in loader.py]
    D --> E[loader.py writes EXEs to temp files]
    E --> F[Run each EXE using threading and subprocess]
    F --> G{Build Single EXE with Nuitka?}
    G -- Yes --> H[main.py builds loader.py into one EXE using Nuitka]
    G -- No  --> I[Proceed without building single EXE]
    H --> J[Output: Single EXE that runs both original programs]
    I --> J
    J --> K[Done]
