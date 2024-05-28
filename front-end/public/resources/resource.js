var questions = [{"role" : "간호사", "question" : "안녕하세요. 어떤 과의 진료를 희망하세요?"}]

function createMessageView(role, message){
    if(role == "chatbot"){
        return `
        <div class="chatbot-log">
                    <div class="log-container">
                        <p>`+message+`</p>
                    </div>
                </div>
        `
    }else{
        return `
        <div class="me-log">
                    <div class="log-container">
                        <p>`+message+`</p>
                    </div>
                </div>
        `
    }
}

function getCategoryFromChatbotAPI(user_input){
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/chatbot/hospital-type?user_input=" + user_input,
        dataType: "json",
        success: function(result) { 
            console.log(result.category)
            $(".chatting-logs-view").append(createMessageView("chatbot", result.category + "로 연결해드리겠습니다"))
            var lastQuestionIdx = localStorage.getItem("last_question_idx")

    /*if(lastQuestionIdx == null){
        lastQuestionIdx = -1
    }

    lastQuestionIdx++
            localStorage.setItem("last_question_idx", lastQuestionIdx)*/
        }
      })
}

function getResponseFromChatbotAPI(user_input){
    var lastQuestionIdx = localStorage.getItem("last_question_idx")

    if(lastQuestionIdx == null){
        lastQuestionIdx = -1
    }

    lastQuestionIdx++

    switch(lastQuestionIdx){
        case 0:
            getCategoryFromChatbotAPI(user_input)
            break
    }

}

$(document).ready(function(){
    $("input[name='query']").on("keydown", function(key){
        if(key.keyCode == 13){
            if($("input[name='query']").val().length == 0){
                alert("응답을 입력하세요")
            }else{
                $(".chatting-logs-view").append(createMessageView("me",$("input[name='query']").val()))
                getResponseFromChatbotAPI($("input[name='query']").val())
                $("input[name='query']").val("")
            }
        }
    })

    $(".chatting-logs-view").scrollTop($('.chatting-logs-view')[0].scrollHeight)

    var lastQuestionIdx = localStorage.getItem("last_question_idx")

    if(lastQuestionIdx == null){
        lastQuestionIdx = -1
    }

    lastQuestionIdx++

    $(".chatting-logs-view").append(createMessageView("chatbot", questions[lastQuestionIdx].question))
})