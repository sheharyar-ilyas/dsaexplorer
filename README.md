# DSA Explorer

An interactive web application for exploring datasets, applying search and filter conditions, learning sorting algorithms, performing multi-level sorting, and comparing algorithm performance.

🌐 **Live Demo:** https://dsaexplorer.streamlit.app/

## Table of Contents

- [Overview](#overview)
- [Project Objectives](#project-objectives)
- [Features](#features)
- [Sorting Algorithms](#sorting-algorithms)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)

## Overview

**DSA Explorer** is an interactive learning project built with Python and Streamlit. It helps users explore datasets and understand how different searching, filtering, and sorting operations work. Users can apply conditions to dataset columns, select sorting algorithms, sort by multiple columns, and compare performance measurements.

The project is designed to make Data Structures and Algorithms (DSA) concepts easier to understand through practical experimentation.

## Project Objectives

- Provide an interactive environment for working with datasets.
- Demonstrate common sorting algorithms using real data.
- Allow users to search and filter data using different conditions.
- Support multi-level sorting, with a separate algorithm and sort order for each level.
- Compare algorithm performance using execution time and available operation counts.
- Connect classroom DSA concepts with practical programming.

## Features

### 1. Dataset Exploration

- View tabular data in an interactive interface.
- Explore rows and columns in the dataset.
- Work with supported dataset sources provided by the application.

### 2. Search and Filter

Filter dataset records using conditions such as:

- Numeric comparisons: equal to, not equal to, greater than, less than, greater than or equal to, and less than or equal to.
- Text conditions: contains, starts with, ends with, and equality.
- Multiple conditions combined with **AND** or **OR**.
- **NOT** to exclude records matching a condition.

The available conditions depend on the selected column's data type.

### 3. Sorting Lab

Experiment with the sorting algorithms implemented in the project. Depending on the algorithm and selected column, the application can show available performance information such as execution time, comparisons, moves/swaps, time complexity, and stability.

### 4. Multi-Level Sorting

Sort a dataset using more than one column. For each sorting level, users can select:

- A column.
- A sorting algorithm.
- Ascending or descending order.

Additional levels can be added or removed. The sort order follows the selected levels: the first level has the highest priority, and later levels sort records that tie on earlier levels.

**Data-type validation:** Counting Sort and Radix Sort require integer data in this application; Bucket Sort is intended for numeric data. If one of these algorithms is selected for an incompatible text column, the application should explain the limitation and ask the user to choose another algorithm.

The implementation should keep complete rows together while sorting, so values from different records are not accidentally mixed. A CSV download is available when supported by the current implementation.

### 5. Benchmarking

Compare supported sorting algorithms using the available benchmark interface. Measurements may include:

- Execution time.
- Comparisons.
- Moves or swaps.
- Time complexity.
- Stability.

Benchmark results depend on the input data, hardware, Python environment, and implementation. Treat execution times as measurements for the tested run rather than universal rankings.

## Sorting Algorithms

The project includes these algorithms:

| Algorithm | General approach |
|---|---|
| Bubble Sort | Repeatedly compares adjacent elements and swaps them when they are out of order. |
| Selection Sort | Repeatedly selects the next smallest or largest element. |
| Insertion Sort | Inserts each element into its correct position in the already-processed part. |
| Merge Sort | Divides the data, sorts the parts, and merges them. |
| Quick Sort | Partitions elements around a pivot and sorts the partitions. |
| Counting Sort | Uses counts of integer values rather than directly comparing every pair. |
| Radix Sort | Sorts numbers digit by digit. |
| Bucket Sort | Distributes numeric values into buckets and sorts the buckets. |

Algorithm availability and supported data types may vary by feature. Check the application's validation messages before choosing an algorithm.

## Technology Stack

- **Python** — application logic and algorithm implementations.
- **Streamlit** — interactive web interface.
- **Pandas** — tabular dataset handling and filtering.
- **Streamlit Community Cloud** — deployment of the live application.

## Project Structure

The structure below is representative. Your repository may use different filenames or folders, so keep this section aligned with the files actually present in GitHub.

```text
dsaexplorer/
├── app.py
├── requirements.txt
├── data_manager.py
├── data/
│   ├── dataset.csv
└──  Sortingalgorithms/
│       ├── bubbleSort.py
│       ├── selectionSort.py
│       ├── insertionSort.py
│       ├── mergeSort.py
│       ├── quickSort.py
│       ├── countingSort.py
│       ├── radixSort.py
│       ├── bucketSort.py
│       └── algorithmsInfo.py
└── views/
    ├── intro.py
    ├── explorer.py
    ├── sorting.py
    ├── multi_sort.py
    └── benchmark.py
```

## Getting Started

### Requirements

- Python 3.10 or a compatible version supported by the project's dependencies.
- Git (optional, if you want to clone the repository).
- The packages listed in `requirements.txt`.

### 1. Clone the repository

Replace the placeholder below with your actual GitHub repository URL.

```bash
git clone https://github.com/sheharyar-ilyas/dsaexplorer.git
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

Use the entry point configured for your project. For example, if `app.py` is the entry point:

```bash
streamlit run app.py
```

If your application is configured to start from another file, use that file instead.

## How to Use

1. Open the live application or run it locally.
2. Explore the available dataset.
3. Use Search and Filter to narrow records using column conditions.
4. Open the Sorting Lab to experiment with the supported algorithms.
5. Use Multi-Level Sorting to choose columns, algorithms, and sort orders for successive levels.
6. Open Benchmarking to compare the measurements available for different algorithms.
7. Download the sorted or filtered data if the relevant download option is available.

## Learning Outcomes

By working with DSA Explorer, users can practise:

- Understanding how sorting algorithms operate.
- Comparing algorithm time complexity and practical performance.
- Recognizing the difference between stable and unstable sorting.
- Understanding in-place and out-of-place sorting concepts.
- Applying conditions to numeric and text data.
- Combining conditions with AND, OR, and NOT.
- Sorting records by multiple columns while preserving row integrity.
- Using Python, Pandas, and Streamlit to build an interactive data application.

## Future Improvements

Possible future additions include:

- More datasets and dataset-upload options.
- Visual, step-by-step animations of sorting algorithms.
- More search algorithms and educational explanations.
- Export options and improved benchmark reports.
- Improved handling of missing values and mixed data types.
- Automated tests for algorithms and multi-level sorting.
- Accessibility and interface improvements.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a branch for your change.
3. Make and test your changes.
4. Submit a pull request describing the improvement.

Please ensure that changes match the project's existing structure and that algorithm outputs are tested before submitting them.

