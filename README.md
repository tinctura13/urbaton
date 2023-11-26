# urbaton
benya3000 forever
К осжалению не успели притащить фронт(
Приложение можно запутстить локально через докер

first you should build container with our app  
```  
docker build -t urbaton-app .
```

then you can run it with
```
docker run -d -p 8080:8080 urbaton-app 
````

api will be available here     
you can try to explore in and have fun ;c  
```
http://0.0.0.0:8080/docs
```

Методв process_image ожидает на вход картинку и нарбо классов для детекции,   
Нужно отпавить эту строку в параметр `classes`
```
{"class_1": 0.09, "class_2": 0.08, "class_3": 0.06, "class_4": 0.06, "class_5": 0.05}
```

Чуть чуть подождать и увидеть результат
