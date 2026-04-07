# MTD Simulator

A simulator used to evaluate moving target defence(MTD) techniques.

## Setup

This guide sets up:

1. A Conda environment named `mtdsim`
2. A Jupyter kernel named `mtdsim`
3. A VS Code workflow for running notebooks

### 1. Install Miniconda 

From your WSL terminal:

```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Close and reopen your WSL terminal after installation.

Initialise Conda in your shell (if needed):

```bash
conda init bash
```

### 2. Create the `mtdsim` environment from `environment.yml`

From the repository root:

```bash
conda config --add channels conda-forge
conda env create -f environment.yml
conda activate mtdsim
```

If the environment already exists and you want to sync to the file:

```bash
conda env update --name mtdsim --file environment.yml --prune
```

### 3. Register a Jupyter kernel named `mtdsim`

After `conda activate mtdsim`:

```bash
python -m ipykernel install --user --name mtdsim --display-name "Python (mtdsim)"
```

This makes the kernel selectable in Jupyter and VS Code notebooks.

### 4. Open notebooks in VS Code (WSL)

1. Open the project in VS Code using the WSL extension.
2. Install the VS Code extensions:
   - Python (`ms-python.python`)
   - Jupyter (`ms-toolsai.jupyter`)
3. Open a notebook in `notebooks/`.
4. Select kernel: **Python (mtdsim)**.

### 5. Verify the environment and kernel

```bash
conda activate mtdsim
python -V
python -c "import networkx, simpy, plotly; print('OK')"
jupyter kernelspec list
```

## Updating Dependencies

After editing `environment.yml`:

```bash
conda env update --name mtdsim --file environment.yml --prune
```

