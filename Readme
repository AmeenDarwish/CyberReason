

#Hello there!

The implementation didnt take me much time and there's a lot to work on but the basic requirements are met i believe.


- [x] Search
- [X] get-planets
- [ ] Unit-testing

## Use:
User only has to create object and call the run method, then run the script.
I've already wrote that in NewHope.py so that it can be run straight from console.
There could be other ways to implement this but this is what i chose for simplicity's sake.
Implementation and instructions are printed out for user so you can check that out there or you can run it and see.



 
## Design:
* The entire implementation was object oriented as it made easier to structure and manage.

* Implementation is user-friendly:
  - uppercase and lowercase support
  - No need for exact matches in search (detailed more below)
  - planet sorting is done in ascending order by default if user didn't state otherwise 
  - detailed documentation
  - bad input proof
  - detailed types in implementation
  
* Object oriented structure allowed me to define private fields and methods in addition to static methods,
  this allowed me to implement a **simple API and keep an eye on security and correct use of the program**.
  
* When user inserts input the input is then passed to a method called that chooses the behavior, this follows
  a design principle known as **single choice principle** that picks from all the options in exactly one place.


* Cache design pattern - Search:
    - The program starts out with just the simple categories,using a few requests.
    - With each search and hence request from SWAPI, the program saves the requested data locally into a cache.
    **This enhances performance and decreases the number of total requests from SWAPI**
    - even if the user makes 10,000 searches, after only a few the program would already have a cache and
      would not make any requests to SWAPI.
    - an upgrade to this could have been done is simply to store the cache on disk after the program is done
    saving future time complexity and allowing us to have the cache ready at all times.

* Cache design pattern - get-planets:
  - On first call, the program will request all the planets from swapi
  - after first call, no requests are made to SWAPI and all planets are saved locally in dictionary by name
  - Before sorting the program will check if the sort has been done before
  - if so it's pulled from dictionary, otherwise it uses the order provided in the command as key for sorting  
  **This enhances performance and decreases the number of total requests from SWAPI**


* ### search accepts any string combination:
  - program requests info from SWAPI until exact match is found
  - if no match is found the program will extract entire search category and then look for relevant results
  Example : "Search people lUKE s" -> will print out Luke Skywalker's profile in addition to any other profile that has
  'luke s' in their search field.
  
  - pro: very useful so that user doesn't have to worry about exactly matching lookup
  - con: heavy performance costs
  ** This is optional and can be removed by commenting out an if-condition of code between 108-124 
    



## Implementation possible upgrades/faults (because of lack of time):
 - when printing out profiles in search, fields that are also resources will appear as links,
 ideally we would want to show them by their search fields as well and not as links
 
 - (same as first issue) if user decided to sort planets by a category that is shown as a link then the sorted python function
 would sort by links and not by actual search field (like sorting by people for example)
 
 - possible fix: adding a private method that gets field from category by index (example: people/1 would be luke skywalker)
   This would make it easier to get the text of search fields that are represented as links, because the links 
   represent them by index.
   This is fairly easy but i am out of time and i have tested my current implementation 
 


## Technical analysis:
   - Saving search fields of results in a dictionary yields the result in constant time O(1)
   On the other hand this costs us O(n*m) SPACE for n fields in m categories
   
   - Having a feature that does not require an exact search field costs O(n) time to find results that are relevant
   and then saving those results requires O(m) space for m number of results until the program prints them and returns
   This feature is very costly, but;
    ### what is a search if we **have to** type in the __exact__ matching of what we're looking for?###
   
   - Caching sorts of planets is extremely efficient as after a few sort commands the program will be able to 
   access each sort(and it's inverse order) in constant time O(1) but this costs us O(n * m) space for n number
   of planets and m number of different sorting keys (sorting order by field)
   The space price we pay for this is justified still, otherwise we are faced with two options:
        1.Only save all planets and then sort them each time:
            - O(n) space
            - O(nlog(n)) time complexity at best: very expensive performance wise
        2.No caching whatsoever,for each sort, planets are requested then sorted:
            - O(n) stack space that disappears after printout (temporary space price)
            - O(nlog(n)) time complexity at best: very expensive performance wise
            - N ticket requests to SWAPI for each sort - hefty price since we're limited to 10k
        
              
   


## Testing:
Although i have no tested because of lack of time but my unit tests would include:
    * Time analysis (for planet sorts especially)
    * Load tests (20k searches for example)
    * Input tests and correctness checks for each category and field
    * Output tests and correctness checks for each category and field
    * command injection 
    * module injection
    * validating imports and dependencies
    * validate SWAPI data for security
    
     





