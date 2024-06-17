<h1 align="center">LogiTyme</h1>
<p align="center">A Python handler for <a href="https://github.com/lmas3009/LogiTyme"><i>logityme</i></a>.</p>

[//]: # ([![python compatibility]&#40;https://github.com/lmas3009/LogiTyme/workflows/Check%20Python%20Package%20Compatiblity%20in%20all%20versions/badge.svg&#41;]&#40;https://github.com/lmas3009/LogiTyme/actions/workflows/Check%20Python%20Package%20Compatiblity%20in%20all%20versions.yml&#41;)
[![python version](https://img.shields.io/badge/Works_With_Python-3.9,%203.10,%203.11-orange)](https://github.com/lmas3009/LogiTyme/actions/workflows/Check%20Python%20Package%20Compatiblity%20in%20all%20versions.yml)

---

LogiTyme is a Python package used to track the time spent on each function, custom functions, and the entire Python Program

- Python package repo link: https://pypi.org/project/LogiTyme/


# *Installation Process*:
1. Install LogiTyme via pip:
To install the LogiTyme package, use the following pip command
    ```bash
    pip install LogiTyme
    ```
3. Verifify the Installation:
After installation, you can verify it by importing LogiTyme in a python script
    ```bash
    import LogiTyme
    print(LogiTyme.__version__)
    ```


# Usage

Simple example on how to use:
```bash
from LogiTyme import LogiTyme

logityme = LogiTyme(env="local")

logityme.StartReport()

def slow_function(n):
  result = 0
  for i in range(n):
    for j in range(n):
      result += i*j
      print(result)

  return result
slow_function(500)

logityme.LogiFuncStart(name="for-loop")
re = 0
for i in range(500):
  for j in range(500):
    re += i * j
    print(re)
logityme.LogiFuncEnd()

logityme.GenerateReport()
```

Resulted Output:
```text
Performance Analysis

1. Introduction:
	This report presents the findings of performance analysis conducted on the python program 'test_main.py'. This purpose of the analysis is to give insights of time consumed by the program and provide recommendations for optimizing the programs's performance

2. Methodolgy:
	The program was profiled using cprofile mmodile to collect data on exection time. The collected data was analyzed to identify functions consuming the most time.

3. Results:
	- Started the program at: 2024-06-14 14:25:01.708068
	- Ended the program at: 2024-06-14 14:25:07.886945
	- Total Execution Time: 6.179 seconds
	- memory consumed: 0.0203MB

4. Functions Results:
+---------------+---------------+
| Function Name | Time Consumed |
+---------------+---------------+
| slow_function | 3.024 secs    |
| for-loop      | 2.65 secs     |
+---------------+---------------+

5. inBuilt-functions Time-Consumed Report:
+----------------------------------+---------------+
| Function Name                    | Time Consumed |
+----------------------------------+---------------+
| <built-in method builtins.print> | 5.253 secs    |
| <built-in method nt.stat>        | 0.001 secs    |
+----------------------------------+---------------+

6. Environment Suggestions:
	- Short tasks (less than 5 minutes):
		-- GCP (Cloud Functions, Compute Engine, GKE, Cloud Run) or AWS (Lambda, EC2, ECS, Step Function, Glue): 
			 Both are well-suited for tasks that complete quickly.
		-- Azure Functions (Consumption Plan, VM, AKS, Container Instances):
			 Good choice for short tasks

7. Code Optimization:
+---------------+---------------+
| Function Name | Time Consumed |
+---------------+---------------+
| slow_function | 3.024 secs    |
| for-loop      | 2.65 secs     |
+---------------+---------------+
The above function "slow_function" is in the 1 position for having highest amount of time in the entire program. Since the function took 3.024 secs is less then 300 seconds (i.e < 5 mins). The function is quite optimized 
The above function "for-loop" is in the 2 position for having highest amount of time in the entire program. Since the function took 2.65 secs is less then 300 seconds (i.e < 5 mins). The function is quite optimized 

8. Conclusion:
	The analysis revealed areas for potential optimization in the Python program 'test_main.py'. By implementing the recommendations outlined in this report, the program's performance can be improved, leading to better overall efficency
```


# Release Version
- **```0.0.1 / 0.0.2```**
  - Launching LogiTyme
    - Functions Included:
      - **StartReport:** _used to start the process of logging the time for you python program._
      - **GenerateReport:**  _used to end the logging process and generate a report based on each function used in the code.
        Now this will start process the logged data and generate a report based on the time spent in each function used in your code.
        The generated report will provide insights into the performance if different functions_
      - **LogiFuncStart & LogiFuncEnd:** _used to log time for custom code._


# *Creator Information*:
- Created By: Aravind Kumar Vemula
- Twitter: https://x.com/AravindKumarV09
- Github: https://github.com/lmas3009

