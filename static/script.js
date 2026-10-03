// ===============================
// QSAR Toxicity Web App Script
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    //-------------------------------
    // Navbar shadow
    //-------------------------------
    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 20) {
            navbar.classList.add("shadow");
        } else {
            navbar.classList.remove("shadow");
        }
    });


    //-------------------------------
    // Active Navigation
    //-------------------------------
    const links = document.querySelectorAll(".nav-link");

    links.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add("active");
        }
    });


    //-------------------------------
    // Card Animation
    //-------------------------------
    const cards = document.querySelectorAll(".card");

    const observer = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if(entry.isIntersecting){
                entry.target.classList.add("show-card");
            }

        });

    },{threshold:0.15});

    cards.forEach(card=>{
        observer.observe(card);
    });


    //-------------------------------
    // File Upload Preview
    //-------------------------------
    const fileInput = document.getElementById("csvFile");

    if(fileInput){

        fileInput.addEventListener("change",function(){

            if(this.files.length>0){

                document.getElementById("file-name").innerHTML =
                    "📄 " + this.files[0].name;

            }

        });

    }


    //-------------------------------
    // Loading Button
    //-------------------------------
    const predictForm = document.getElementById("predict-form");

    if(predictForm){

        predictForm.addEventListener("submit",function(){

            const btn = document.getElementById("predictBtn");

            btn.disabled = true;

            btn.innerHTML =
            `<span class="spinner-border spinner-border-sm"></span>
             Predicting...`;

        });

    }


    //-------------------------------
    // Counter Animation
    //-------------------------------
    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter=>{

        counter.innerText=0;

        const updateCounter=()=>{

            const target=+counter.getAttribute("data-target");

            const c=+counter.innerText;

            const increment=target/100;

            if(c<target){

                counter.innerText=Math.ceil(c+increment);

                setTimeout(updateCounter,20);

            }
            else{

                counter.innerText=target;

            }

        }

        updateCounter();

    });


    //-------------------------------
    // Copy SMILES
    //-------------------------------
    const copyBtn=document.getElementById("copySmiles");

    if(copyBtn){

        copyBtn.addEventListener("click",()=>{

            const smiles=document.getElementById("smiles");

            navigator.clipboard.writeText(smiles.value);

            showToast("SMILES copied!");

        });

    }


    //-------------------------------
    // Toast Message
    //-------------------------------
    function showToast(message){

        let toast=document.createElement("div");

        toast.className="toast-message";

        toast.innerHTML=message;

        document.body.appendChild(toast);

        setTimeout(()=>{
            toast.classList.add("show");
        },100);

        setTimeout(()=>{
            toast.classList.remove("show");

            setTimeout(()=>{
                toast.remove();
            },500);

        },2500);

    }


    //-------------------------------
    // Dark Mode
    //-------------------------------
    const toggle=document.getElementById("darkToggle");

    if(toggle){

        if(localStorage.getItem("theme")==="dark"){

            document.body.classList.add("dark");

            toggle.innerHTML="☀️";

        }

        toggle.addEventListener("click",()=>{

            document.body.classList.toggle("dark");

            if(document.body.classList.contains("dark")){

                localStorage.setItem("theme","dark");

                toggle.innerHTML="☀️";

            }else{

                localStorage.setItem("theme","light");

                toggle.innerHTML="🌙";

            }

        });

    }


    //-------------------------------
    // Smooth Scroll
    //-------------------------------
    document.querySelectorAll('a[href^="#"]').forEach(anchor=>{

        anchor.addEventListener("click",function(e){

            e.preventDefault();

            document.querySelector(this.getAttribute("href"))
            ?.scrollIntoView({
                behavior:"smooth"
            });

        });

    });

});
