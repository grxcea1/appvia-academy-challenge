import sys # this module lets me access the arguments
level = sys.argv[1]  # this gets the log info from the first argument
file_path = sys.argv[2] # this lets me get the file name from the second argument

counts ={} # empty dictionary that i will use to store the counts

with open(file_path, "r" ) as file: # this opens the files and reads it
    for line in file: #for loop to go through the file line by line to check each log entry
        line = line. strip() #this just removes any whitespace 

        if not line: #this skips empty lines 
            continue

        parts = line.split() # splits the lines into seperate parts

        if len(parts) < 4: #if the line has less then 4 parts it is in the wrong format
            continue # skips invalid line
    
        service = parts[1] # gets service name from the line
        log_level = parts[2] # sets the level from the line

        if log_level == level: # checks the log level matches the one we want exactly "=="
            counts[service] = counts.get(service, 0) + 1 #adds one to the services count each count starting from 0

results = sorted(counts.items(), key=lambda item: (-item[1], item[0])) # sorts by count then by service name 

for service, count in results: 
    print(f"{service}: {count}") # prints each service and its count