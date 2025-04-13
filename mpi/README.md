# MPI aplikace - práce s kolektivními operacemi
- navrhněte paralelizovatelnou matematickou úlohu, kterou lze řešit v prostředí MPI
- používejte vstup a výstup dat ze souborů
- v řešení použijte redukční operace pro sběr výsledků
- master node zobrazí výsledný soubor

# How to run

Tested with python 3.9

1. Install MPI deps (MacOS)
    ```bash
    brew install mpich
    ```
2. Clone the repository
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run (without input.txt 1 billion samples is default)
   ```bash
    mpiexec -n 4 python pi.py input.txt
    ```

# Example of output in [result.txt](./result.txt):
```
Number of processes: 4
Total samples: 100000000
pi estimate: 3.14138688
True pi value: 3.141592653589793
Error: 0.0002057735897929014
Execution time: 0.37 seconds
```