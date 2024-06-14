
/* modal buttons */
const modal = document.getElementById('myModal');
const modal_p = document.getElementById('myModal-p')
const modal_btn = document.getElementById('myModal-btn')

const settings = JSON.parse(sessionStorage.getItem("simpleAuthSettings"));



function redirect(url){
    console.log(settings.base_url);

    window.location.replace(settings.base_url + url);
}

function logout_btn_onclick(){
    fetch('/auth/logout', {
        method: "POST",
    })
    .then(r => {
        if(r.status == 200){
            open_modal_ok("Please check your inbox now")
        }else{
            open_modal_close("Something went wrong. Please try again later.")
        }
    })

    window.location.replace("login");

}

function chpass_btn_onclick(){
    var oldpass = document.getElementById('oldpassword').value;
    var pass = document.getElementById('newpassword').value;
    var pass2 = document.getElementById('newpassword2').value;

    if(oldpass == '' || pass == '' || pass2 == ''){
        open_modal_close("Please fill all the fields.")
        return    
    }

    if(pass != pass2){
        open_modal_close("Passwords do not match.")
        return
    }

    const payload = {
        'old_password': oldpass,
        'password': pass,
    }

    fetch('/auth/change_password', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify(payload)
    })
    .then(r => {
        console.log(r);
        console.log(r.status);
        switch(r.status){
            case 200:
                open_modal_ok("password changed");
                break;
            case 401:
                open_modal_close("Incorrect password.");
                break;
            default:
                open_modal_close("Something went wrong. Please try again later.")
        }
    })
}


function open_modal(msg, btn_classes = null, btn_title = null, btn_onclick=null){
    modal_p.innerHTML = msg

    /* clear classes */

    modal_btn.classList.remove('is-warning');
    modal_btn.classList.remove('is-danger');
    modal_btn.classList.remove('is-success');

    if(btn_classes){
        modal_btn.classList.add(...btn_classes)
    }

    if(btn_title){
        modal_btn.innerText = btn_title
    }

    if(btn_onclick){
        modal_btn.onclick = btn_onclick;
        // console.log(modal_btn)
    }

    modal.classList.add('is-active');
}

function open_modal_close(msg){
    open_modal(msg, ['is-warning'], 'Close');
}

function open_modal_ok(msg, onclick = null){
    open_modal(msg, ['is-success'], 'OK', onclick);
}

const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };

function verify_btn_onclick(){

    var code = document.getElementById('code').value;

    const payload = {
        'code': code,
    }

    /* all checks passed */
    fetch(window.location.href, {
        method: "POST",    
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify(payload)
    })
    .then(async r => {
        switch(r.status){
            case 200:
                var result = await r.json();
                open_modal_ok("Verification successful", function() { window.location.replace(result['url']); } );
                break;
            case 400:
                open_modal_close(await r.text());
                break;
            default:
                open_modal_close("System error (try reloading page): " + await r.text());
                break;
        }
    })
}

function recover_btn_onclick(){
    const code = document.getElementById('code').value
    const password = document.getElementById('password').value
    const password2 = document.getElementById('password2').value

    const segments = window.location.href.split('/');
    const email = segments[segments.length - 1];

    console.log(email);

    // verify if code, password are valid
    if(! code || ! password || ! password2){
        open_modal_close("Please fill all the fields.")
        return
    }

    // if passwords match
    if(password != password2){
        open_modal_close("Passwords do not match.")
        return
    }

    const payload = {
        'code': code,
        'password': password
    }

    fetch('', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify(payload)
    })
    .then(async r => {
        console.log(r);
        console.log(r.status);
        switch(r.status){
            case 200:
                open_modal_ok("Changed password, login now", function() { redirect('/login'); } );
                break;
            case 400:
                open_modal_close(await r.text());
                break;
            default:
                open_modal_close("Something went wrong. Please try again later.")
        }
    })


}

function send_recover_btn_onclick(){

    const username = document.getElementById('username').value

    if(! username){
        open_modal_close("Email address not be empty")
    }
    if(! validateEmail(username)){
        open_modal_close("Invalid email address")
    }

    const payload = {
        'email': username
    }
    fetch('recover', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify(payload)
    })
    .then(async r => {
        console.log(r);
        console.log(r.status);
        switch(r.status){
            case 200:
                open_modal_ok(await r.text());
                break;
            case 429:
                open_modal_close("Code was sent recently, cannot resend now");
                btn.disabled = true;
                break;
            default:
                open_modal_close("Something went wrong. Please try again later.")
        }
    })
}

function verify_resend_btn_onclick(){

    const segments = window.location.href.split('/');
    const email = segments[segments.length - 1];

    const btn = document.getElementById("fastapi-simple-auth-verify-resend-btn")

    fetch('/auth/emailverify_resend/' + email, {
        method: "POST",
    })
    .then(async r => {
        console.log(r);
        console.log(r.status);
        switch(r.status){
            case 200:
                open_modal_ok(await r.text());
                break;
            case 429:
                open_modal_close("Code was sent recently, cannot resend now");
                btn.disabled = true;
                break;
            default:
                open_modal_close("Something went wrong. Please try again later.")
        }
    })    
  }


  function login_btn_onclick(){
    var username_el = document.getElementById('username')
    var username = username_el.value
    var pass1 = document.getElementById('password').value
    
    var response;

    if(! username){
        open_modal_close("Username must not be empty");
        return
    }

    if(! pass1){
        open_modal_close("Password must not be empty");
        return
    }

    const user_el = document.getElementById('username')
    const pass_el = document.getElementById('password')

    const formData = new FormData();
    formData.append("username", user_el.value);
    formData.append("password", pass_el.value);

    /* all checks passed */
    fetch('/auth/login', {
        method: "POST",    
        body: formData,
        // redirect: 'manual'
    })
    .then(async r => {
        console.log(r);

        switch(r.status){
            case 200:
                var result = await r.json();
                window.location.replace(result['url']);
                break;
            case 401:
                var result = await r.json();
                open_modal_close(result.detail);
                pass_el.value = "";
                break;
            default:
                open_modal_close("System error (try reloading page): " + await r.text());
                break;
        }
    })
    .catch(e => console.log("MYERROR", e))
}
  

function reg_btn_onclick(){
    const username_el = document.getElementById('username') 
    const username = username_el.value
    const pass1 = document.getElementById('password').value
    const pass2 = document.getElementById('password2').value

    var response;


    if(! username){
        open_modal_close("Username must not be empty");
        return
    }

    if(username_el.classList.contains("email") && ! validateEmail(username)){
        open_modal_close("Username must be valid email");        
    }

    if(! pass1){
        open_modal_close("Password must not be empty");
        return
    }

    if(pass1 != pass2){
        open_modal_close("Password and verification do not match");
        return
    }

    const payload = {
        'username': username,
        'password': pass1
    }

    /* all checks passed */
    fetch('/auth/users/', {
        method: "POST",    
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify(payload)
    })
    .then(r => {
        response = r.clone();
        return r.json();
    })
    .then(async r => {
        // console.log("FIN", r, response.status, response)

        switch(response.status){
            case 200:
                window.location = r.redirect;
                break;
            case 400:
                open_modal_close(r.detail);
                break;
            default:
                open_modal_close("Something went wrong. Please try again later.")
        }

    })
    .catch(e => console.log("ERROR", e))
}

function init_hooks(){
    var hooks = {
        'fastapi-simple-auth-register-btn': reg_btn_onclick,
        'fastapi-simple-auth-login-btn': login_btn_onclick,
        'fastapi-simple-auth-logout-btn': logout_btn_onclick,
        'fastapi-simple-auth-verify-btn': verify_btn_onclick,
        'fastapi-simple-auth-verify-resend-btn': verify_resend_btn_onclick,
        'fastapi-simple-auth-chpass-btn': chpass_btn_onclick,
        'fastapi-simple-auth-send-recover-btn': send_recover_btn_onclick,
        'fastapi-simple-auth-recover-btn': recover_btn_onclick,
    }
    for (let el_id in hooks) {
        var btn = document.getElementById(el_id);
        if(btn){
            // console.log("hook", el_id, btn)
            btn.onclick = hooks[el_id]
        }
    }
    
}

function init_page(){

    const closeModalButtons = document.querySelectorAll('.closeModal, .modal-background, .modal-close');

    closeModalButtons.forEach(button => {
        button.addEventListener('click', () => {
        modal.classList.remove('is-active');
        });
    });

    init_hooks();
}

init_page()