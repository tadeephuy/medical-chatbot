# medical-chatbot

## Installation
    google-trans-new==1.1.9

## Usage

**1. Query Entity**  
The script to map given (intent,[entities]) is in `src/main.py`  
The extracted KB is in `cancer_data/final_kb.json`

Example: `python main.py`   
```     
mapper = Mapper('../cancer_data/final_kb.json')
ans = mapper.query('symptom',['thalassemia','ung thư gan',"buồn nôn"])
```
Output:
```
thalassemia : mệt mỏi
thalassemia : mệt mỏi
thalassemia : không có triệu chứng
ung thư gan : giảm cân mà không cần cố gắng
ung thư gan : giảm cân mà không cần cố gắng
ung thư gan : ăn mất ngon
buồn nôn : ung thư gan
buồn nôn : ung thư gan
```
**2. Build KB**
All the scripts for KB are in `cancer_data/`  

There are 2 steps:   
1. Build english kb from file `data.json` to export `database.json`  
    ```python build_kb.py```
        
2. Build vietnamese kb . Output is `final_kb.json`   

    ```python translate.py```

**3. Get symptoms entities**   
```    
    cd src/  
    python utils.py
```

## Future work
-   Entity Linking to enrich Vietnamese KB 
-   Argument inputs
-   Refactor
-   Load balancer for KB access