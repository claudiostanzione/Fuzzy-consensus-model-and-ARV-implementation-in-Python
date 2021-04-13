# Fuzzy-consensus-model-and-ARV-implementation-in-Python
Master's degree exam
TRACK: Implement Fuzzy Consensus Model (FCM) and Average Rating Values(ARV)algorithmas a Python program.

Requests:
1.The input for the program is represented by a set of text files (CSV format) containing fuzzy preference relationmatrices of a given set of experts, a first additional file containing experts’ names and experts’ weights and a second additional file containing alternatives.
2.Additional inputis  represented  by FCMparameters  like maximum  number  of  rounds, consensus threshold, lambda1, lambda2, etc.
3.The outputof the program is represented by all the results (final and intermediate) offered by FCM (consensus building) and ARV (ranking).
4.The program must be interactivefor the end-user, thus it should ask for file namesandinput parameters, communicate the consistencyof fuzzy preference relation matrices, ask to change suchmatricesalong the consistency check or the feedback mechanism, provide results on the standard output, etc
5.The program must work with any numberof expertsand alternatives
6.The program must be organized in Python functions(you can reuse common functions written for the homework#1).
7.The program must use NumPy (Pandas is not requiredfor this homework).

Test casesProvide also two sets of input (files and other info) to test your program:
1.A first example that does not require the feedback mechanism
2.A second example that requires the feedback mechanism In  at  least  one  of  the  above  test  cases,  please  demonstrate  that  the  consistency  check  works  well. Provide also a text document in which all the steps to execute your code are described in detailsand the test cases are explained and documented.

Python tools
•Use NumPy to handle all vector-based structures and operations.
•Use  Spyder  (in  the  Anaconda  package)  to  write  the  program.You  must  create  a  Spyder Project.


Relation on work done:
The code starts with the request of the folder name where are placed the files with the preferences of the experts. In this case is necessary to insert only the name of the folder, is also necessary that all the files with the expert alternatives are in this folder. The files are required in csv format. In the project are provided two test cases, one about a campaign of marketing and another about the recruiting campaign. The folder name are for marketing: “marketing” and for recruiting: “recruiting”.  After this is required the threshold value of consensus that the user prefers, is important for the feedback mechanism. The advice is to insert for the marketing a threshold of 0.85, so is possible test the feedback mechanism, while for the recruting the consensus is so high and for active a feedback mechanism is necessary a threshold greater than 0.91. 
After this are required to provide the two lambda values, in this case is necessary to insert for the building of groups for feedback mechanism. For all two case tests the advice is to set lambda1:”0.35” and lambda2: “0.25”, but is only an advice,every lambda value is allowed. 
Other input is the number of rounds for avoid loops in case the programm enters in the feedback mechanism and consensus is not  reached up. 
Now are required two csv file that contain the names of the experts and their weights and in other file the alternatives names. For the markting campaign the file names are: “marketingweights.csv” and “marketingalternatives.csv” , for recruiting campaign file names are: “recruitingweights.csv” and “recruitingalternatives.csv”.
After all this output the application strarts, the expert preferences are read and put into an array. Second step is the control of the matrixes, the check of the reciprocal and consistency check. Here also one of the matrixes is not consistent the user can choose if continue the same or change the values. In both test cases the consistency is not reached up and then is necessary continue without. 
First output are the similarity matrixes that are ordered following the order of experts , in case of marketing campaign the order is:(1-2; 1-3; 1-4; 2-3; 2-4; 3-4), the number of matrixes is equal to coefficient binomial that is calculated but not given in output.  
Next output is the consensus matrix. After this output if the consensus is not ok are given in output the collective preference matrixes(pc matrix),  the collective similarity matrixes(pp matrixes) and collective similarity measure and after the consensus value. If not necessary the feedback mechanism after the consensus matrix is showed the consensus value.
If the application enters in the feedback mechanism are showed the advices for each expert, in particular for each pair of alternative the advice can be: “increase”, “decrease” and “not change”, the expert can follow this advices or not. After this advices is required the new folder name with files changed or not. If all the experts don’t change is possible to provide the same folder name of the initial input. If is not appreciated the feedback mechanism when required set the number of rounds in zero. This feedback mechanism is repeated until the consensus is reached up or the the limit of the rounds is reached up. For the test case marketing campaing in the project are provided two folder with some values changed with the advices given by the application, and folders names are “marketing2” and “marketing3” . Every time that feedback mechanism runs are showed the same output described previously and then also the consensus value. 
After the feedback mechanism the application goes to calculate the best alternative with the average rating values method.  Is showed the mean of each alternative for each expert. With this values ordered is assigned to each alternative a score,if the values are equal is assigned the same score. This final score is given in output with the corresponding alternatives names. Last output is the name of the best alternative.
Marketing campaign is documented in the excel file: “Marketing fuzzy analysis.xlsx”
Recruiting campaign is documented in the excel file: “Recruiting fuzzy analysis.xlsx”
