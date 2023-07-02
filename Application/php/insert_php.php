<?php 

    error_reporting(E_ALL); 
    ini_set('display_errors',1); 

    include('android_log_php.php');



    if (($_SERVER['REQUEST_METHOD'] == 'POST') && isset($_POST['submit']))
    {

        $useremail=$_POST['useremail'];
        $userid=$_POST['userid'];
        $userpw=$_POST['userpw'];
        $userpw_ch=$_POST['userpw_ch'];
        $userphone=$_POST['userphone'];
        $username=$_POST['username'];
        $userdate=$_POST['userdate'];
        $useranswer=$_POST['useranswer'];
        $userquestion=$_POST['userquestion'];
        $usercreated = date("Y-m-d H:i:s");
        


        if(empty($useremail)){
            $errMSG = "이메일을 입력하세요.";
        }
        else if(empty($userid)){
            $errMSG = "아이디를 입력하세요.";
        }
        else if(empty($userpw)){
            $errMSG = "비밀번호를 입력하세요.";
        }

        else if(empty($userphone)){
            $errMSG = "핸드폰 번호를 입력하세요.";
        }
        else if(empty($username)){
            $errMSG = "이름을 입력하세요.";
        }
        else if(empty($userdate)){
            $errMSG = "생년월일을 입력하세요.";
        }
        
        else if(!empty($_POST['userquestion'])){ //콤보박스의 값을 가져왔는데 비어있지 않으면
            $selectd =$_POST['userquestion']; //$selectd라는 변수에 선택한 콤보박스의 값 userquetion을 담는다.
            $question_default = "- 질문을 선택해주세요 -"; //콤보박스를 아무것도 건들이지 않았을때 값을 question_default로 생각하여 - 질문을 선택해주세요 - 값을 넣었다.
            if($selectd == $question_default){ //선택한 콤보박스의 값이 - 질문을 선택해주세요 - 즉, 아무것도 선택안했을 경우에
                $errMSG = "질문을 선택해주세요.";
            }
        
        }
        
        else if(empty($useranswer)){
            $errMSG = "질문의 답을 입력하세요.";
        }

        else if($userpw != $userpw_ch ){
            $errMSG = "비밀번호가 같지 않습니다.";
        }


        



        if(!isset($errMSG)) //$errMSG가 존재하지 않았을 경우
        {
            try{ //try , catch
                $stmt = $con->prepare('INSERT INTO users(useremail, userid, password,userphone, username, userdate, userquestion, useranswer, usercreated)
                 VALUES(:useremail,:userid, :userpw, :userphone , :username, :userdate,  :userquestion, :useranswer, :usercreated )');
                $stmt->bindParam(':useremail', $useremail);
                $stmt->bindParam(':userid', $userid);
                $stmt->bindParam(':userpw', $userpw);
                $stmt->bindParam(':userphone', $userphone);
                $stmt->bindParam(':username', $username);
                $stmt->bindParam(':userdate', $userdate);
                $stmt->bindParam(':userquestion', $userquestion);
                $stmt->bindParam(':useranswer', $useranswer);
                $stmt->bindParam(':usercreated', $usercreated);



                if($stmt->execute())
                {
                    
                    $successMSG = "새로운 사용자를 추가했습니다.";
                }
                else
                {
                    $errMSG = "사용자 추가 에러";
                }

            } catch(PDOException $e) { //PHP와 MySQL 연동은 성공하였으나 DB 오류가 났을때
 
       
                
                die("Database error: " . $e->getMessage()); 
            }
        }

    }
?>

<html>
<body>



<?php 

        if (isset($errMSG)) { //만약 $errMSG의 변수의 값이 존재할 경우 
            // 자바 스크립트의 alert를 이용하여 팝업창에 $errMSG를 띄운다.
         echo   "<script>      
         alert('{$errMSG}');
         </script>";         
        }
        
        if (isset($successMSG)){ //만약 $$successMSG 변수의 값이 존재할 경우 
       // 자바 스크립트의 alert를 이용하여 팝업창에 $successMSG 띄운다.
        echo   "<script>      
        alert('{$successMSG}');
        </script>";
        }

        ?>
      


<form action="<?php $_PHP_SELF ?>" method="POST">
                <h1>회원가입 창</h1>
                  <!-- 일반적인 입력 형태 -->
                <p><input type="email" name="useremail" id="useremail" placeholder="E-mail"></p>
                <p><input type="text" name="userid" id="userid" placeholder="ID"></p>
                <p><input type="password" name="userpw" id="userpw" placeholder="Password"></p>
                <p><input type="password" name="userpw_ch" id="userpw_ch" placeholder="Password Check"></p>
                <p><input type="text" name="userphone" id="userphone" placeholder="Phone Number 000-0000-0000"></p>
                <p><input type="text" name="username" id="username" placeholder="Name"></p>
                <p><input type="date" name="userdate" id="userdate" placeholder="Date"></p>

                <!-- 콤보 박스를 이용하였습니다. name 속성을 이용하여 콤보박스 안에 있는 것들을 하나로 묶어주었습니다.  -->
                <select name = "userquestion" onchange ="userquestion_selectchangebox(this.value);"> 
                    <option value = "- 질문을 선택해주세요 -" selected>- 질문을 선택해주세요 -</option>
                    <option value = "당신의 별명은 무엇입니까?">당신의 별명은 무엇입니까?</option>
                    <option value = "당신의 아버지의 성함은?">당신의 아버지의 성함은?</option>
                    <option value = "당신의 보물 1호는?">당신의 보물 1호는?</option>
                    <option value = "당신의 고향은?">당신의 고향은?</option>
                    <option value = "당신이 감명깊게 읽은 책은?">당신이 감명깊게 읽은 책은?</option>
                 </select>

                <p><input type="text" name="useranswer" id="useranswer" placeholder="Answer"></p>

            <input type = "submit" name = "submit" />
        </form>
</body>
</html>

<?php
        
        ?>