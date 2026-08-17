# Write-up: [Grace Adio]

## What was broken
 I started by reading the README and then tried to get the application running. I used the error messages, the README specification and the behaviour of the application to work through the problems one at a time.

1. app would not start
- Where: app/package.json
- What I noticed: When I ran npm start, the app could not find index.js.
- Why it was happening: The npm start command was trying to run index.js, but the actual app file was called server.js.
- What I changed: I changed the start command in package.json so that it points to server.js.
- How I investigated it: I checked the error message and then looked at the files in the app folder. There was no index.js, but there was a server.js, so I checked package.json because the npm start command is defined there.

2. missing morgan dependency
- Where: app
- what I noticed: in the error message the morgan module couldn't be found.
- Why it was happening: Morgan was being used by the app but was not installed.
- What I changed: I installed the missing dependency and tried starting the application again.
- How I investigated it: I used the error message to identify the missing module.

3. incorret default port
- Where: server.js
- What I noticed: The application was using port 300 instead of port 3000 mentioned in the README.
- Why it was happening: The port in the app was not the same as the README specification, and the app also needed to allow the port to be changed using the PORT environment variable.
- What I changed:
const port = process.env.PORT || 3000;

This means that if a PORT environment variable is provided, the app will use it and if not then the default is 3000.

- How I investigated it: I knew what the README required, but I was not familiar with the Node.js syntax for environment variables. I searched for how Node.js applications can use an environment variable with a default value and used that information to understand the change.


4. Empty todos were accepted
- Where: server.js, POST /api/todos
- What I noticed: I was able to add empty todos in the web UI. A blank todo was created and the server returned 201.
- Why it was happening: There was no validation to check if text was put in before creating the todo.
- What I changed: I added a check so that an empty or missing text value returns 400 Bad Request.

if (!text) {
    return res.status(400).json({ error: 'Text is required' });
}

- How I investigated it: I first tested the application through the web UI because the README said that an empty todo should be rejected. I then looked at the POST code. I used ChatGPT to explain the existing code to me because I did not know the syntax of nodejs. This helped me understand where the validation needed to go. I then tested the change again.


5. PUT couldnt find real todos
- Where: server.js, PUT /api/todos/:id
- What I noticed: When I tried to mark a real todo as done, the application returned 404, even though the todo existed.
- Why it was happening: The ID sent from the URL was a string, while the IDs stored in the application were numbers. The code was using strict equality, so the values were not the same.
- What I changed: I converted the ID from the URL into a number using:

Number(req.params.id)

- How I investigated it: I knew the todo existed because I had just created it. so i looked at the ID being used to find it. I used ChatGPT to help me understand what type of value was given to route parameters. I then looked up how to convert the value to a number and used Number().


6. DELETE deleted the wrong todo 
- Where: server.js, DELETE /api/todos/:id
- What I noticed: The DELETE request returned 204, which looked correct, but it deleted the wrong todo. it deleted the one before the one I had picked.
- Why it was happening: The code was passing the todo ID directly to splice(). However, splice() works using the position of an item in an array, not the item's ID.
- What I changed: I used findIndex() to find the position of the todo with the requested ID and then passed that position to splice(). I also converted the URL ID to a number when comparing it with the stored IDs.
- How I investigated it: The HTTP status was correct, but the actual behaviour was wrong this is why i decided to check the code. I searched for how splice() works and learned that it uses an array index. I then looked up findIndex() and used it to find the correct position before deleting the todo.

After making these changes, I tested the main functionality again through the application.


## 2. Security concerns

- The main security issue I found was that the ADMIN_TOKEN was written directly in the application code and used by the /api/admin/reset endpoint.

- This endpoint can delete all of the todos. Because the token is stored in the source code, anyone with access to the code could potentially see the token and use it to access the admin functionality.

-  I did not change this during the assessment because I wasn't confident that I could implement a proper authentication solution correctly within the time available. I felt it was better to identify the security issue rather than make a change that I didn't fully understand.

-  I would remove the secret from the source code and use a proper secret management solution. I would also make sure the admin endpoint has appropriate authentication and authorisation.

-  I also noticed vulnerability warnings when I ran npm install, but focused first on getting the application working according to the specification. I then considered the security issues separately.


## 3. How to run my submission

- App: `cd app && npm install && npm start` (The app runs on port 3000 by default but different port can be used using the PORT environment variable)
- Log tool: I created the required analyse.sh file.
The script is run using: `./analyse.sh <LEVEL> <path-to-log-file>` (must be run from a terminal compatible with Bash) (written in python)

-I chose Python for the main logic because I have previous experience with Python and felt more comfortable understanding and testing the solution in Python.


## 4. My top three production improvements

Exactly three, in priority order, with your reasoning for both the choice and
the order.

1. proper secret management and authentication
- The application currently has a hardcoded admin token which protects an endpoint that can delete all of the todos
- I would remove the secret from the source code and use proper secret management. I would also make sure the admin endpoint has appropriate authentication and authorisation.
- I put this first because it is a security issue and the endpoint can perform a destructive action. I think protecting that functionality should come before making other improvements.


2. automated tests
- I would add automated tests for the API, especially around the problems I found during the assessment.
- Tests I would add:
    - An empty todo should return 400.  
    - An existing todo should be able to be toggled.
    - A non-existent ID should return 404.
    - Deleting a todo should delete the correct todo.
- I chose this as the second priority because some of the bugs I found could have been caught by automated tests. They would also give more confidence that future changes don't accidentally break existing functionality.


3. Saving todos in a database
- The application currently stores the todos in memory. I would change this so the todos are saved in a database.
-  At the moment, the todos would be lost if the application was restarted. Saving them in a database would mean they are still available after a restart.
-  I think this would be important for a real application, but I would deal with the security issue first and then add automated tests before making these changes.

## 5. Optional extensions (if attempted)

- I did not attempt an optional extention as i decided to focus on completing the core requirements first.

## 6. How I used AI tools
- I used ChatGPT throughout the assessment as a learning and troubleshooting tool.
- For Part 1, I used it to help me understand unfamiliar Node.js and Express code and work out why some of the existing code was not behaving as expected.
- For Part 2, I used it more heavily because I had not written a log analysis program before. I used it to help me understand the requirements and how to implement them in Python.
- I also used Google and documentation when I needed to understand specific concepts.
- I tested the code myself and checked the results against the requirements rather than assuming the suggestions from AI were always right.
- I made sure I understood the code I submitted and could explain the main decisions I made.

## 7. Reflections

- The hardest part of the exercise was understanding code I had not written myself and working out why it did not work how it was supposed to. 
- I found that testing the problem first made it easier to understand what was going wrong.
- I learned the importance of understanding existing code before making changes.
- I also became more comfortable using Python to analyse log files.
- If I had another day, I would add automated tests, save the todo data in a database, and improve the application's security.
