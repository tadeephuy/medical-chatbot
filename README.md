## Define REST API

### Installation
    python>=3.6
    torch==1.6.0
    transformers==3.0.2
    seqeval==0.0.12
    pytorch-crf==0.7.2

Trained `phobert` checkpoint can be download here : https://drive.google.com/drive/folders/1-O68dwR3QzKtIsjNFX2lZ5FqhrQ0IN5g?usp=sharing  
(Vu has higher accuracy model. Please update the model path)

Note : if transformer==3.0.2 bug --> use ==4.5.1  


### Usage 

### Inference API
    `python define_format_api.py`

format : 
```
{   
    "mess": "tao muốn biết triệu chứng về bệnh ung thư gan .",
    "_id": 1
}
```
Method : POST  
url = 'http://127.0.0.1:5000/proc-nlu'  
```
{
    "_id": 1,
    "mess": "tao muốn biết triệu chứng về bệnh ung thư gan .",
    "predict": {
        "entities": [
            [
                "O",
                "O",
                "O",
                "O",
                "O",
                "O",
                "O",
                "B-BỆNH",
                "I-BỆNH",
                "I-BỆNH",
                "O"
            ]
        ],
        "intent": {
            "class": "symptoms",
            "confidence": 0.9999309778213501
        }
    },
    "status": 200
}
```
url = 'http://127.0.0.1:5000/proc-nlu-kb'
Method : POST
```
{
    "_id": 1,
    "mess": "tao muốn biết triệu chứng về bệnh ung thư gan .",
    "predict": {
        "answer_entity": "giảm cân mà không cần cố gắng",
        "entity": "ung thư gan",
        "intent": "symptom",
        "original_text": "hầu hết mọi người không có dấu hiệu và triệu chứng trong giai đoạn đầu của ung thư gan nguyên phát. khi các dấu hiệu và triệu chứng xuất hiện, chúng có thể bao gồm: giảm cân mà không cần cố gắng ăn mất ngon đau bụng trên buồn nôn và ói mửa điểm yếu và mệt mỏi chung sưng bụng sự đổi màu vàng của làn da của bạn và lòng trắng mắt của bạn (vàng da) phân trắng, phấn"
    },
    "status": 200
}
```
#### Testing

Call request POSTMAN


{\
    "mess": text,\
    "id" : id\
}

URL endpoint: localhost:????/proc-nlu\
Attribute: POST
