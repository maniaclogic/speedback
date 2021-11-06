# speedback

1. add file called speedback_participants.txt in the same folder
2. add people and rooms seperated by commas and linebreaks
    ``` 
    Participant A, https://zoom.us/my/kat
    Participant B, https://teams.microsoft.com/
     ```
3. the script prioritises zoom rooms by default if you want to choose a persons room 100% of the time add `priority;`
  ```
  Participant A, https://zoom.us/my/kat
  Participant B, priority; https://chime.aws.com/
  ```
4. when running the script it will promt you for the start time in military time. `1340` 
Forgo this by hardcoding the string in the script.

