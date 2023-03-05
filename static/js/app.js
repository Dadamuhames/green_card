let clearBtn = document.getElementById("clear-btn");
let clearModal = document.getElementById("clear-modal");
let clearWrap = document.getElementById("clear-wrap");
let clearCancel = document.getElementById("clear-cancel");

if (clearBtn) {
  clearBtn.addEventListener("click", () => {
    clearModal.classList.add("show");
  });
}
if (clearWrap) {
  clearWrap.addEventListener("click", () => {
    clearModal.classList.remove("show");
  });
}
if (clearCancel) {
  clearCancel.addEventListener("click", () => {
    clearModal.classList.remove("show");
  });
}

let sidebar = document.getElementById("sidebar");

sidebar.addEventListener("mouseover", () => {
  sidebar.classList.add("open");
});
sidebar.addEventListener("mouseleave", () => {
  sidebar.classList.remove("open");
});

var x, i, j, l, ll, selElmnt, a, b, c;
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < ll; j++) {
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function (e) {
      var y, i, k, s, h, sl, yl;
      s = this.parentNode.parentNode.getElementsByTagName("select")[0];
      sl = s.length;
      h = this.parentNode.previousSibling;
      for (i = 0; i < sl; i++) {
        if (s.options[i].innerHTML == this.innerHTML) {
          s.selectedIndex = i;
          h.innerHTML = this.innerHTML;
          y = this.parentNode.getElementsByClassName("same-as-selected");
          yl = y.length;
          for (k = 0; k < yl; k++) {
            y[k].removeAttribute("class");
          }
          this.setAttribute("class", "same-as-selected");
          break;
        }
      }
      h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function (e) {
    e.stopPropagation();
    closeAllSelect(this);
    this.nextSibling.classList.toggle("select-hide");
    this.classList.toggle("select-arrow-active");
  });
}
function closeAllSelect(elmnt) {
  var x,
    y,
    i,
    xl,
    yl,
    arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i);
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
document.addEventListener("click", closeAllSelect);

let filterBtn = document.getElementById("filter-btn");
let filterBody = document.getElementById("filter-body");
let resetBtn = document.getElementById("reset-btn");

if (filterBtn) {
  filterBtn.addEventListener("click", () => {
    filterBody.classList.toggle("show");
    resetBtn.style.color = "blue";
  });
}

let settingBtn = document.getElementById("setting-btn");
let settingBody = document.getElementById("setting-body");

if (settingBtn) {
  settingBtn.addEventListener("click", () => {
    settingBody.classList.toggle("show");
  });
}

let createBtn = document.getElementById("create-btn");
let createX = document.getElementById("create-x");
let createBody = document.getElementById("create-body");
let createCancel = document.getElementById("create-cancel");
// let mainLayout = document.getElementById("main-layout");

if (createBtn) {
  createBtn.addEventListener("click", () => {
    createBody.classList.add("show");
  });
}
if (createX) {
  createX.addEventListener("click", () => {
    createBody.classList.remove("show");
  });
}
if (createCancel) {
  createCancel.addEventListener("click", () => {
    createBody.classList.remove("show");
  });
}

let editBtns = document.querySelectorAll(".redactors");
let editBody = document.getElementById("edit-body");
let editX = document.getElementById("edit-x");
let editCancel = document.getElementById("edit-cancel");

editBtns.forEach((editBtn) => {
  editBtn.addEventListener("click", (e) => {
    let id = $(e.target).attr('data-user')
    console.log(id)
    
    $.ajax({
      url: '/get_user',
      type: 'GET',
      data: {'id': id},
      datatype: 'json',
      success: (data) => {
        console.log(data)
        $('#edit-body').find('[name="name"]').val(data.name)
        $('#edit-body').find('[name="username"]').val(data.user.username)
        $('#edit-body').find('[name="nbm"]').val(data.nbm)
        $('#edit-body').find(`option[value=${data.status}]`).prop("selected", true)
        $('#edit-body').find(`option[value=${data.filial}]`).prop("selected", true)
        $('#edit-body').find('[name="id"]').val(data.user.id)

        console.log($('#edit-body').find(`option[value=${data.filial}]`))
      }
    })
    editBody.classList.add("show");
  });
});

if (editX) {
  editX.addEventListener("click", () => {
    editBody.classList.remove("show");
  });
}

if (editCancel) {
  editCancel.addEventListener("click", () => {
    editBody.classList.remove("show");
  });
}

var element = document.getElementById("num");
var maskOptions = {
  mask: "+{998}(00)000-00-00",
};
var mask = IMask(element, maskOptions);

const tabs = document.querySelectorAll("[data-target]"),
  tabContents = document.querySelectorAll("[data-content]");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const target = document.querySelector(tab.dataset.target);

    tabContents.forEach((tabContent) => {
      tabContent.classList.remove("active");
    });
    target.classList.add("active");
    tabs.forEach((tab) => {
      tab.classList.remove("active");
    });
    tab.classList.add("active");
  });
});

const tabs1 = document.querySelectorAll("[data-goal]"),
  tabContents1 = document.querySelectorAll("[data-body]");

tabs1.forEach((tab1) => {
  tab1.addEventListener("click", () => {
    const target1 = document.querySelector(tab1.dataset.goal);

    tabContents1.forEach((tabContent1) => {
      tabContent1.classList.remove("active");
    });
    target1.classList.add("active");
    tabs1.forEach((tab1) => {
      tab1.classList.remove("active");
    });
    tab1.classList.add("active");
  });
});

let addBtn = document.getElementById("add-btn");
let addBody = document.getElementById("add-body");
let addX = document.getElementById("add-x");

if (addBtn) {
  addBtn.addEventListener("click", () => {
    addBody.classList.add("show");
  });
}
if (addX) {
  addX.addEventListener("click", () => {
    addBody.classList.remove("show");
  });
}

let openBtn = document.getElementById("open-btn");
let openBody = document.getElementById("open-body");
let openX = document.getElementById("open-x");

if (openBtn) {
  openBtn.addEventListener("click", () => {
    openBody.classList.add("show");
  });
}
if (openX) {
  openX.addEventListener("click", () => {
    openBody.classList.remove("show");
  });
}
$(document).ready(function () {
  $(".js-example-basic-single").select2();
});

let fillerBtn = document.getElementById("filler-btn");
let fillerBody = document.getElementById("filler");
let fillerX = document.getElementById("filler-x");
let fillerCancel = document.getElementById("filler-cancel");

if (fillerBtn) {
  fillerBtn.addEventListener("click", () => {
    fillerBody.classList.add("show");
  });
}
if (fillerX) {
  fillerX.addEventListener("click", () => {
    fillerBody.classList.remove("show");
  });
}
if (fillerCancel) {
  fillerCancel.addEventListener("click", () => {
    fillerBody.classList.remove("show");
  });
}
let docTitles = document.querySelectorAll(".doc__title");
let docLists = document.querySelectorAll(".doc__list");

const tabs2 = document.querySelectorAll("[data-button]"),
  tabContents2 = document.querySelectorAll("[data-list]");

tabs2.forEach((tab2) => {
  tab2.addEventListener("click", () => {
    const target = document.querySelector(tab2.dataset.button);

    tabContents2.forEach((tabContent2) => {
      tabContent2.classList.remove("active");
    });
    target.classList.add("active");
    tabs2.forEach((tab2) => {
      tab2.classList.remove("active");
    });
    tab2.classList.add("active");
  });
});



$('#page-size-form').on("change", () => {
  $('#page-size-form').submit()
})


