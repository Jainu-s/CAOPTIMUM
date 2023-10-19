import os
import pandas as pd


def visualization():
    # Directory paths
    base_dir = r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot"
    passed_dir = os.path.join(base_dir, "Test Case Passed")
    failed_dir = os.path.join(base_dir, "Test Case Failed")
    testcases_dir = r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Testcases"

    # Function to check if folder has an image
    def has_image(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    return True
        return False

    # Data collection for table
    data = []

    for subfolder in os.listdir(passed_dir):
        subfolder_path = os.path.join(passed_dir, subfolder)
        if os.path.isdir(subfolder_path) and has_image(subfolder_path):
            image_path = next(file for root, dirs, files in os.walk(subfolder_path)
                              for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')))
            full_image_path = os.path.join(subfolder_path, image_path)
            data.append([subfolder, "✔️", full_image_path])

    for subfolder in os.listdir(failed_dir):
        subfolder_path = os.path.join(failed_dir, subfolder)
        if os.path.isdir(subfolder_path) and has_image(subfolder_path):
            image_path = next(file for root, dirs, files in os.walk(subfolder_path)
                              for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')))
            full_image_path = os.path.join(subfolder_path, image_path)
            data.append([subfolder, "❌", full_image_path])

    # Go through the test case files and update the 'Actual Results'
    for file in os.listdir(testcases_dir):
        file_path = os.path.join(testcases_dir, file)
        if not file.startswith("~") and file.endswith(".xlsx"):
            df = pd.read_excel(file_path, engine='openpyxl')

            print('df:',df)

            # Find the appropriate 'id' column in a generic way
            id_col = None
            for col in df.columns:
                if 'id' in col.lower():
                    id_col = col
                    break

            if id_col is None:
                raise ValueError("No ID-like column found in the Excel sheet.")

            for index, row in df.iterrows():
                case_id = str(row[id_col])
                actual_result = row['Actual Results']

                for entry in data:
                    if entry[0] == case_id:
                        entry[1] = "✔️" if actual_result == "Passed" else "❌"

    # Data collection for bar chart
    total_test_cases = len(data)
    passed_test_cases = sum(1 for entry in data if entry[1] == "✔️")
    failed_test_cases = total_test_cases - passed_test_cases

    # HTML generation
    html = """
       <html>
       <head>
           <title>Test Cases Dashboard</title>
           <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
           <style>
               body {
                   font-family: Arial, sans-serif;
                   background-color: #ffffff;
                   color: #000000;
                   margin: 50px;
               }
               .chart-container {
                   width: 60%;
                   height: 400px;
                   margin: 20px auto;
               }
               table {
                   width: 80%;
                   margin: 30px auto;
                   border-collapse: collapse;
                   background-color: #f2f2f2;
               }
               th, td {
                   padding: 15px;
                   text-align: left;
                   border-bottom: 1px solid #aaaaaa;
               }
               th {
                   background-color: #007BFF;
                   color: white;
                   border-bottom: 2px solid #888888;
               }
               tr:nth-child(even) {
                   background-color: #e6e6e6;
               }
           </style>
       </head>
       <body>
           <h2>Test Cases Dashboard</h2>

           <div class="chart-container">
               <canvas id="testCaseChart"></canvas>
           </div>

           <table>
               <thead>
                   <tr>
                       <th>Test Case No</th>
                       <th>Status</th>
                       <th>Image Path</th>
                   </tr>
               </thead>
               <tbody>
       """

    for entry in data:
        html += "<tr>"
        html += f"<td>{entry[0]}</td>"
        html += f"<td>{entry[1]}</td>"
        html += f"<td><a href=\"file://{entry[2]}\">{entry[2]}</a></td>"
        html += "</tr>"
    # Finish table and add Chart.js code
    html += """
            </tbody>
        </table>

        <script>
            var ctx = document.getElementById('testCaseChart').getContext('2d');

            var gradientGray = ctx.createLinearGradient(0, 0, 0, 400);
            gradientGray.addColorStop(0, '#cccccc');
            gradientGray.addColorStop(1, '#888888');

            var gradientGreen = ctx.createLinearGradient(0, 0, 0, 400);
            gradientGreen.addColorStop(0, '#aaffaa');
            gradientGreen.addColorStop(1, '#00cc00');

            var gradientRed = ctx.createLinearGradient(0, 0, 0, 400);
            gradientRed.addColorStop(0, '#ffaaaa');
            gradientRed.addColorStop(1, '#cc0000');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Total Test Cases', 'Test Cases Passed', 'Test Cases Failed'],
                    datasets: [{
                        data: [""" + str(total_test_cases) + """, """ + str(passed_test_cases) + """, """ + str(failed_test_cases) + """],
                        backgroundColor: [gradientGray, gradientGreen, gradientRed],
                        barPercentage: 0.5,
                        categoryPercentage: 0.7,
                        borderRadius: 10
                    }]
                },
                options: {
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0,
                                color: '#000000'
                            },
                            grid: {
                                display: false
                            }
                        },
                        x: {
                            ticks: {
                                color: '#000000'
                            },
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });

        </script>
    </body>
    </html>
    """

    with open(r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Reports\dashboard.html", "w",
              encoding="utf-8") as f:
        f.write(html)

    print("Dashboard updated with Actual Results!")

visualization()










#
# import os
#
# def visualization():
#     # Directory paths
#     base_dir = r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot"
#     passed_dir = os.path.join(base_dir, "Test Case Passed")
#     failed_dir = os.path.join(base_dir, "Test Case Failed")
#
#     # Function to check if folder has an image
#     def has_image(folder_path):
#         for root, dirs, files in os.walk(folder_path):
#             for file in files:
#                 if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
#                     return True
#         return False
#
#     # Data collection for bar chart
#     total_test_cases = len(os.listdir(passed_dir)) + len(os.listdir(failed_dir))
#     passed_test_cases = sum(
#         [1 for subfolder in os.listdir(passed_dir) if has_image(os.path.join(passed_dir, subfolder))])
#     failed_test_cases = sum(
#         [1 for subfolder in os.listdir(failed_dir) if has_image(os.path.join(failed_dir, subfolder))])
#
#     # Data collection for table
#     data = []
#
#     for subfolder in os.listdir(passed_dir):
#         subfolder_path = os.path.join(passed_dir, subfolder)
#         if os.path.isdir(subfolder_path) and has_image(subfolder_path):
#             image_path = next(file for root, dirs, files in os.walk(subfolder_path)
#                               for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')))
#             full_image_path = os.path.join(subfolder_path, image_path)
#             data.append((subfolder, "✔️", full_image_path))
#
#     for subfolder in os.listdir(failed_dir):
#         subfolder_path = os.path.join(failed_dir, subfolder)
#         if os.path.isdir(subfolder_path) and has_image(subfolder_path):
#             image_path = next(file for root, dirs, files in os.walk(subfolder_path)
#                               for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')))
#             full_image_path = os.path.join(subfolder_path, image_path)
#             data.append((subfolder, "❌", full_image_path))
#
#     # HTML generation
#     html = """
#     <html>
#     <head>
#         <title>Test Cases Dashboard</title>
#         <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#         <style>
#             body {
#                 font-family: Arial, sans-serif;
#                 background-color: #ffffff;
#                 color: #000000;
#                 margin: 50px;
#             }
#             .chart-container {
#                 width: 60%;
#                 height: 400px;
#                 margin: 20px auto;
#             }
#             table {
#                 width: 80%;
#                 margin: 30px auto;
#                 border-collapse: collapse;
#                 background-color: #f2f2f2;
#             }
#             th, td {
#                 padding: 15px;
#                 text-align: left;
#                 border-bottom: 1px solid #aaaaaa;
#             }
#             th {
#                 background-color: #007BFF;
#                 color: white;
#                 border-bottom: 2px solid #888888;
#             }
#             tr:nth-child(even) {
#                 background-color: #e6e6e6;
#             }
#         </style>
#     </head>
#     <body>
#         <h2>Test Cases Dashboard</h2>
#
#         <div class="chart-container">
#             <canvas id="testCaseChart"></canvas>
#         </div>
#
#         <table>
#             <thead>
#                 <tr>
#                     <th>Test Case No</th>
#                     <th>Status</th>
#                     <th>Image Path</th>
#                 </tr>
#             </thead>
#             <tbody>
#     """
#
#
#     # Inserting table rows with the new column for image paths
#     for entry in data:
#         html += "<tr>"
#         html += f"<td>{entry[0]}</td>"
#         html += f"<td>{entry[1]}</td>"
#         html += f"<td><a href=\"file://{entry[2]}\">{entry[2]}</a></td>"
#         html += "</tr>"
#
#     # Finish table and add Chart.js code
#     html += """
#             </tbody>
#         </table>
#
#         <script>
#             var ctx = document.getElementById('testCaseChart').getContext('2d');
#
#             var gradientGray = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientGray.addColorStop(0, '#cccccc');
#             gradientGray.addColorStop(1, '#888888');
#
#             var gradientGreen = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientGreen.addColorStop(0, '#aaffaa');
#             gradientGreen.addColorStop(1, '#00cc00');
#
#             var gradientRed = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientRed.addColorStop(0, '#ffaaaa');
#             gradientRed.addColorStop(1, '#cc0000');
#
#             new Chart(ctx, {
#                 type: 'bar',
#                 data: {
#                     labels: ['Total Test Cases', 'Test Cases Passed', 'Test Cases Failed'],
#                     datasets: [{
#                         data: [""" + str(total_test_cases) + """, """ + str(passed_test_cases) + """, """ + str(failed_test_cases) + """],
#                         backgroundColor: [gradientGray, gradientGreen, gradientRed],
#                         barPercentage: 0.5,
#                         categoryPercentage: 0.7,
#                         borderRadius: 10
#                     }]
#                 },
#                 options: {
#                     plugins: {
#                         legend: {
#                             display: false
#                         }
#                     },
#                     scales: {
#                         y: {
#                             beginAtZero: true,
#                             ticks: {
#                                 precision: 0,
#                                 color: '#000000'
#                             },
#                             grid: {
#                                 display: false
#                             }
#                         },
#                         x: {
#                             ticks: {
#                                 color: '#000000'
#                             },
#                             grid: {
#                                 display: false
#                             }
#                         }
#                     }
#                 }
#             });
#
#         </script>
#     </body>
#     </html>
#     """
#
#     # Save HTML to file
#     with open(r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Reports\dashboard.html", "w", encoding="utf-8") as f:
#         f.write(html)
#
#     print("Dashboard generated!")
#
# # Now, you can call the visualization function
# visualization()
#
























# import os
#
#
# def visualization():
#     # Directory paths
#     base_dir = r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot"
#     passed_dir = os.path.join(base_dir, "Test Case Passed")
#     failed_dir = os.path.join(base_dir, "Test Case Failed")
#
#     # Function to check if folder has an image
#     def has_image(folder_path):
#         for root, dirs, files in os.walk(folder_path):
#             for file in files:
#                 if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
#                     return True
#         return False
#
#     # Data collection for bar chart
#     total_test_cases = len(os.listdir(passed_dir)) + len(os.listdir(failed_dir))
#     passed_test_cases = sum(
#         [1 for subfolder in os.listdir(passed_dir) if has_image(os.path.join(passed_dir, subfolder))])
#     failed_test_cases = sum(
#         [1 for subfolder in os.listdir(failed_dir) if has_image(os.path.join(failed_dir, subfolder))])
#
#     # Data collection for table
#     data = []
#
#     for subfolder in os.listdir(passed_dir):
#         subfolder_path = os.path.join(passed_dir, subfolder)
#         if os.path.isdir(subfolder_path) and has_image(subfolder_path):
#             data.append((subfolder, "✔️"))
#
#     for subfolder in os.listdir(failed_dir):
#         subfolder_path = os.path.join(failed_dir, subfolder)
#         if os.path.isdir(subfolder_path) and has_image(subfolder_path):
#             data.append((subfolder, "❌"))
#
#     # HTML generation
#     html = """
#     <html>
#     <head>
#         <title>Test Cases Dashboard</title>
#         <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#         <style>
#             body {
#                 font-family: Arial, sans-serif;
#                 background-color: #ffffff;
#                 color: #000000;
#                 margin: 50px;
#             }
#             .chart-container {
#                 width: 60%;
#                 height: 400px;
#                 margin: 20px auto;
#             }
#             table {
#                 width: 80%;
#                 margin: 30px auto;
#                 border-collapse: collapse;
#                 background-color: #f2f2f2;
#             }
#             th, td {
#                 padding: 15px;
#                 text-align: left;
#                 border-bottom: 1px solid #aaaaaa;
#             }
#             th {
#                 background-color: #007BFF;
#                 color: white;
#                 border-bottom: 2px solid #888888;
#             }
#             tr:nth-child(even) {
#                 background-color: #e6e6e6;
#             }
#         </style>
#     </head>
#     <body>
#         <h2>Test Cases Dashboard</h2>
#
#         <div class="chart-container">
#             <canvas id="testCaseChart"></canvas>
#         </div>
#
#         <table>
#             <thead>
#                 <tr>
#                     <th>Test Case No</th>
#                     <th>Status</th>
#                 </tr>
#             </thead>
#             <tbody>
#     """
#
#     # Inserting table rows
#     for entry in data:
#         html += "<tr>"
#         html += f"<td>{entry[0]}</td>"
#         html += f"<td>{entry[1]}</td>"
#         html += "</tr>"
#
#     # Finish table and add Chart.js code
#     html += """
#             </tbody>
#         </table>
#
#         <script>
#             var ctx = document.getElementById('testCaseChart').getContext('2d');
#
#             var gradientGray = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientGray.addColorStop(0, '#cccccc');
#             gradientGray.addColorStop(1, '#888888');
#
#             var gradientGreen = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientGreen.addColorStop(0, '#aaffaa');
#             gradientGreen.addColorStop(1, '#00cc00');
#
#             var gradientRed = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientRed.addColorStop(0, '#ffaaaa');
#             gradientRed.addColorStop(1, '#cc0000');
#
#             new Chart(ctx, {
#                 type: 'bar',
#                 data: {
#                     labels: ['Total Test Cases', 'Test Cases Passed', 'Test Cases Failed'],
#                     datasets: [{
#                         data: [""" + str(total_test_cases) + """, """ + str(passed_test_cases) + """, """ + str(failed_test_cases) + """],
#                         backgroundColor: [gradientGray, gradientGreen, gradientRed],
#                         barPercentage: 0.5,
#                         categoryPercentage: 0.7,
#                         borderRadius: 10
#                     }]
#                 },
#                 options: {
#                     plugins: {
#                         legend: {
#                             display: false
#                         }
#                     },
#                     scales: {
#                         y: {
#                             beginAtZero: true,
#                             ticks: {
#                                 precision: 0,
#                                 color: '#000000'
#                             },
#                             grid: {
#                                 display: false
#                             }
#                         },
#                         x: {
#                             ticks: {
#                                 color: '#000000'
#                             },
#                             grid: {
#                                 display: false
#                             }
#                         }
#                     }
#                 }
#             });
#
#         </script>
#     </body>
#     </html>
#     """
#
#     # Save HTML to file
#     with open(r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Reports\dashboard.html", "w", encoding="utf-8") as f:
#         f.write(html)
#
#     print("Dashboard generated!")
#
#
# # Now, you can call the visualization function
# visualization()

# Black Background Report


# import os
#
# def visualization():
#     # Directory paths
#     base_dir = r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot"
#     passed_dir = os.path.join(base_dir, "Test Case Passed")
#     failed_dir = os.path.join(base_dir, "Test Case Failed")
#
#     # Function to check if folder has an image
#     def has_image(folder_path):
#         for root, dirs, files in os.walk(folder_path):
#             for file in files:
#                 if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
#                     return True
#         return False
#
#     # Data collection for bar chart
#     total_test_cases = len(os.listdir(passed_dir)) + len(os.listdir(failed_dir))
#     passed_test_cases = sum([1 for subfolder in os.listdir(passed_dir) if has_image(os.path.join(passed_dir, subfolder))])
#     failed_test_cases = sum([1 for subfolder in os.listdir(failed_dir) if has_image(os.path.join(failed_dir, subfolder))])
#
#     # Data collection for table
#     data = []
#
#     for subfolder in os.listdir(passed_dir):
#         subfolder_path = os.path.join(passed_dir, subfolder)
#         if os.path.isdir(subfolder_path) and has_image(subfolder_path):
#             data.append((subfolder, "✔️"))
#
#     for subfolder in os.listdir(failed_dir):
#         subfolder_path = os.path.join(failed_dir, subfolder)
#         if os.path.isdir(subfolder_path) and has_image(subfolder_path):
#             data.append((subfolder, "❌"))
#
#     # HTML generation
#     html = """
#     <html>
#     <head>
#         <title>Test Cases Dashboard</title>
#         <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#         <style>
#             body {
#                 font-family: Arial, sans-serif;
#                 background-color: #000;
#                 color: #eaeaea;
#                 margin: 50px;
#             }
#             .chart-container {
#                 width: 60%;
#                 height: 400px;
#                 margin: 20px auto;
#             }
#             table {
#                 width: 80%;
#                 margin: 30px auto;
#                 border-collapse: collapse;
#                 background-color: #1a1a1a;
#             }
#             th, td {
#                 padding: 15px;
#                 text-align: left;
#                 border-bottom: 1px solid #555;
#             }
#             th {
#                 background-color: #007BFF;
#                 color: white;
#                 border-bottom: 2px solid #444;
#             }
#             tr:nth-child(even) {
#                 background-color: #101010;
#             }
#         </style>
#     </head>
#     <body>
#         <h2>Test Cases Dashboard</h2>
#
#         <div class="chart-container">
#             <canvas id="testCaseChart"></canvas>
#         </div>
#
#         <table>
#             <thead>
#                 <tr>
#                     <th>Test Case No</th>
#                     <th>Status</th>
#                 </tr>
#             </thead>
#             <tbody>
#     """
#
#     # Inserting table rows
#     for entry in data:
#         html += "<tr>"
#         html += f"<td>{entry[0]}</td>"
#         html += f"<td>{entry[1]}</td>"
#         html += "</tr>"
#
#     # Finish table and add Chart.js code
#     html += """
#             </tbody>
#         </table>
#
#         <script>
#             var ctx = document.getElementById('testCaseChart').getContext('2d');
#
#             var gradientGray = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientGray.addColorStop(0, 'white');
#             gradientGray.addColorStop(1, 'gray');
#
#             var gradientGreen = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientGreen.addColorStop(0, 'lightgreen');
#             gradientGreen.addColorStop(1, 'green');
#
#             var gradientRed = ctx.createLinearGradient(0, 0, 0, 400);
#             gradientRed.addColorStop(0, 'pink');
#             gradientRed.addColorStop(1, 'red');
#
#             new Chart(ctx, {
#                 type: 'bar',
#                 data: {
#                     labels: ['Total Test Cases', 'Test Cases Passed', 'Test Cases Failed'],
#                     datasets: [{
#                         data: [""" + str(total_test_cases) + """, """ + str(passed_test_cases) + """, """ + str(failed_test_cases) + """],
#                         backgroundColor: [gradientGray, gradientGreen, gradientRed],
#                         barPercentage: 0.5,
#                         categoryPercentage: 0.7,
#                         borderRadius: 10
#                     }]
#                 },
#                 options: {
#                     plugins: {
#                         legend: {
#                             display: false
#                         }
#                     },
#                     scales: {
#                         y: {
#                             beginAtZero: true,
#                             ticks: {
#                                 precision: 0,
#                                 color: '#ffffff'
#                             }
#                         },
#                         x: {
#                             ticks: {
#                                 color: '#ffffff'
#                             }
#                         }
#                     }
#                 }
#             });
#
#
#
#         </script>
#     </body>
#     </html>
#     """
#
#     # Save HTML to file
#     with open(r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Reports\dashboard.html", "w", encoding="utf-8") as f:
#         f.write(html)
#
#     print("Dashboard generated!")


















# import os
#
# # Directory path
# dir_path = "Screenshot"
#
# # Function to check if folder has an image
# def has_image(folder_path):
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
#                 return True
#     return False
#
# # Gather data
# data = []
# for subfolder in os.listdir(dir_path):
#     subfolder_path = os.path.join(dir_path, subfolder)
#     if os.path.isdir(subfolder_path):
#         if has_image(subfolder_path):
#             data.append((subfolder, "Failed"))
#         else:
#             data.append((subfolder, "Passed"))
#
# # Calculate statistics
# total_subfolders = len(data)
# empty_subfolders = sum(1 for _, status in data if status == "Passed")
# subfolders_with_images = sum(1 for _, status in data if status == "Failed")
#
# # Begin HTML generation
# html = """
# <html>
# <head>
#     <title>Test Cases Dashboard</title>
#     <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             background-color: #f5f5f5;
#             margin: 50px;
#         }
#         .chart-container {
#             width: 50%; /* Adjust width as per preference */
#             margin: 20px auto;
#         }
#         table {
#             width: 100%;
#             border-collapse: collapse;
#             background-color: #ffffff;
#             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#         }
#         th, td {
#             padding: 15px;
#             text-align: left;
#         }
#         th {
#             background-color: #007BFF;
#             color: white;
#             border-bottom: 2px solid #444;
#         }
#         tr:nth-child(even) {
#             background-color: #f2f2f2;
#         }
#         td {
#             border-bottom: 1px solid #ddd;
#         }
#     </style>
# </head>
# <body>
#     <h2>Test Cases Dashboard</h2>
#     <div class="chart-container">
#         <canvas id="myChart"></canvas>
#     </div>
#     <table>
#         <thead>
#             <tr>
#                 <th>Test Case No</th>
#                 <th>Test Case Passed</th>
#                 <th>Test Case Failed</th>
#             </tr>
#         </thead>
#         <tbody>
# """
#
# # Inserting table rows
# for entry in data:
#     html += "<tr>"
#     html += f"<td>{entry[0]}</td>"
#     if entry[1] == "Passed":
#         html += f"<td>✔️</td><td></td>"
#     else:
#         html += f"<td></td><td>❌</td>"
#     html += "</tr>"
#
# # Continue HTML generation after table
# html += """
#         </tbody>
#     </table>
#
#     <script>
#         const ctx = document.getElementById('myChart').getContext('2d');
#         const myChart = new Chart(ctx, {
#             type: 'bar',
#             data: {
#                 labels: ['Total Test Cases', 'Test Cases Successful', 'Test Cases Failed'],
#                 datasets: [{
#                     label: '# of Subfolders',
#                     data: [""" + str(total_subfolders) + """, """ + str(empty_subfolders) + """, """ + str(subfolders_with_images) + """],
#                     backgroundColor: [
#                         'rgba(255, 99, 132, 0.2)',  // Pink for Total Subfolders
#                         'rgba(75, 192, 192, 0.2)',  // Green for Empty Subfolders
#                         'rgba(255, 0, 0, 0.2)'      // Red for Subfolders with Images
#                     ],
#                     borderColor: [
#                         'rgba(255, 99, 132, 1)',    // Pink for Total Subfolders
#                         'rgba(75, 192, 192, 1)',    // Green for Empty Subfolders
#                         'rgba(255, 0, 0, 1)'        // Red for Subfolders with Images
#                     ],
#                     borderWidth: 1
#                 }]
#             },
#             options: {
#                 scales: {
#                     y: {
#                         beginAtZero: true
#                     }
#                 }
#             }
#         });
#     </script>
# </body>
# </html>
# """
#
# # Save HTML to file
# with open("dashboard.html", "w", encoding="utf-8") as f:
#     f.write(html)
#
# print("Enhanced dashboard generated!")






















# import os
#
# # Directory paths
# base_dir = r"C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot"
# passed_dir = os.path.join(base_dir, "Test Case Passed")
# failed_dir = os.path.join(base_dir, "Test Case Failed")
#
# # Function to check if folder has an image
# def has_image(folder_path):
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
#                 return True
#     return False
#
# # Gather data
# data = []
#
# # For "Test Case Passed"
# for subfolder in os.listdir(passed_dir):
#     subfolder_path = os.path.join(passed_dir, subfolder)
#     if os.path.isdir(subfolder_path):
#         if has_image(subfolder_path):
#             data.append((subfolder, "Test Case Passed"))
#
# # For "Test Case Failed"
# for subfolder in os.listdir(failed_dir):
#     subfolder_path = os.path.join(failed_dir, subfolder)
#     if os.path.isdir(subfolder_path):
#         if has_image(subfolder_path):
#             data.append((subfolder, "Test Case Failed"))
#
# # Begin HTML generation
# html = """
# <html>
# <head>
#     <title>Test Cases Dashboard</title>
#     <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             background-color: #000;
#             color: #eaeaea;
#             margin: 50px;
#         }
#         .chart-container {
#             width: 50%;
#             margin: 20px auto;
#         }
#         table {
#             width: 100%;
#             border-collapse: collapse;
#             background-color: #1a1a1a;
#             box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
#         }
#         th, td {
#             padding: 15px;
#             text-align: left;
#             border-bottom: 1px solid #555;
#         }
#         th {
#             background-color: #007BFF;
#             color: white;
#             border-bottom: 2px solid #444;
#         }
#         tr:nth-child(even) {
#             background-color: #101010;
#         }
#         @keyframes fadeIn {
#             0% {opacity: 0;}
#             100% {opacity: 1;}
#         }
#         tr {
#             animation-name: fadeIn;
#             animation-duration: 1s;
#             animation-fill-mode: both;
#         }
#         tr:nth-child(n+1) {
#             animation-delay: 0.2s;
#         }
#         tr:nth-child(n+2) {
#             animation-delay: 0.4s;
#         }
#     </style>
# </head>
# <body>
#     <h2>Test Cases Dashboard</h2>
#     <table>
#         <thead>
#             <tr>
#                 <th>Test Case No</th>
#                 <th>Test Case Passed</th>
#                 <th>Test Case Failed</th>
#             </tr>
#         </thead>
#         <tbody>
# """
#
# # Inserting table rows
# for entry in data:
#     html += "<tr>"
#     html += f"<td>{entry[0]}</td>"
#     if entry[1] == "Test Case Passed":
#         html += f"<td>✔️</td><td></td>"
#     else:
#         html += f"<td></td><td>❌</td>"
#     html += "</tr>"
#
# # Finish HTML generation
# html += """
#         </tbody>
#     </table>
# </body>
# </html>
# """
#
# # Save HTML to file
# with open("dashboard.html", "w", encoding="utf-8") as f:
#     f.write(html)
#
# print("Dashboard generated!")


















