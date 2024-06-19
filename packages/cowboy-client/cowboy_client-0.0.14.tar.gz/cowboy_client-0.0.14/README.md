```
pip install cowboy
```

First create a .user file in the root directory to represent a new user. It should contain your email and OpenAI API key
```
### .user
email: helloworld@gmail.com
openai_api_key: sk-K***********************7
```

Initialize your user
```
cowboy user init
```

Next create a YAML repo config
```
repo_name: "test_repo"
url: https://github.com/JohnPeng47/codecov-cli-neuteured.git
cov_folders: ["codecov_cli"]
interp: python          # path to your Python interpreter on your local computer
```

Create the repo
```
cowboy repo create test_repo.yaml
```
