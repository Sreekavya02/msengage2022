# msengage2022
-> Languages used :  <br />
   front-end - html,css,js <br />
   backend - django
   algorithm - python
-> Main logic of the application i.e; algorithms to recommend movies (content based filtering) and movies classification (and suggestion) based on genres is in 
    my_app/algorithm.py file
-> Model is created by processing 5000 Movies dataset collected from tmdb
-> to run the application in your local system run command 
    python manage.py runserver
-> Api key used to fetch movie details of a particular movie with it's id is 
    9efcaddf4cc2015dfec426a229f2768d (tmdb)
->  Password hashers used - bcrypt,django[argon2]
-> This is my first website building so bugs frequently gave me a hard time but I took on those challenges and learnt many things while resolving them
-> Application performance(server response speed) can be increased if we store all these details of movies in movie model rather than fetching it from an api 
    (couldn't implement this because there are only 10 days to do this project because of my semester exams till May 19)

-> References followed = https://developers.google.com/machine-learning/recommendation/content-based/basics
                         https://www.youtube.com/watch?v=OTmQOjsl0eg&t=7117s   (django learning)
                         https://www.templateshub.net/template/FlixGo-Online-Movies-Template
                         

