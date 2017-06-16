# Chronicle

##### This repo is for my tech blog project.    


### Quick Start
-Clone the repo: `git clone https://github.com/ianagpawa/tech-blog.git`


#### Dependencies
This app requires `google app engine (python)` and `gcloud` installed on your system. Additionally, the following third-party libraries are also required and should be listed in file `requirements.txt` located in the root directory:
```
Flask==0.12.1
google-cloud-datastore==0.22.1
gunicorn==19.6.0
```
File `appengine_config.py` in the root directory is used to specify where to look for third-party libraries.  To install dependencies:
1. Install `virtualenv` on your local machine (Linux):
```
$   sudo apt get install virtualenv
```
2. Enter isolated Python environment:
```
$   virtualenv env
$   source env/bin/activate
```

3. Install third-party libraries:
```
$   pip install -t lib -r requirements.txt
```

4.  You can exit the isolated Python environment at this point.
```
$   deactivate
```


#### Viewing the app locally
While the terminal is in the root directory, run the following command:
```
$   dev_appserver.py .
```


### File structure
Within the project folder, you will find the following files:

```
tech-blog/
    ├── .git/ (NOT INCLUDED)
    ├── env/  (NOT INCLUDED)
    ├── lib/  (NOT INCLUDED)
    ├── static/
    |    └── css/
    |        └──  style.css
    ├── templates/
    |    ├── base.html
    |    ├── delete_post.html
    |    ├── edit_post.html
    |    ├── front.html
    |    ├── login.html
    |    ├── new_post.html
    |    ├── post_L.html
    |    ├── post.html
    |    └── signup.html
    ├── .gitignore
    ├── app.yaml
    ├── appengine_config.py
    ├── config.py
    ├── main.py
    ├── Post.py
    ├── README.md
    ├── requirements.txt
    ├── User.py
    └── WelcomePage.py
```

## Creator

**Ian Agpawa**


[Github](https://github.com/ianagpawa)

 agpawaji@gmail.com
