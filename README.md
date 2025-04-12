# Hello, I'm EQ.

Hi!  
I tried to make a program that compiles multiple programs into one, called **Binder**.  
I'm not very good at English — all of this is done using Google Translate.  
If you understand something or have questions, please [Email me](mailto:dexedusd@gmail.com)

## Workflow Diagram - EXE Binder

```mermaid
graph TD
    A[Start] --> B[User Inputs EXE File One and Two or via args]
    B --> C[embed_files.py reads EXE files as bytes]
    C --> D[Generate embedded dict in loader.py]
    D --> E[loader.py writes EXEs to temp files]
    E --> F[Run each EXE using threading and subprocess]
    F --> G[main.py optionally builds loader.py into one EXE using Nuitka]
    G --> H[Output: Single EXE that runs both original programs]
    H --> I[Done]
    
