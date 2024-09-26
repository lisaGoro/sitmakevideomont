const fileUploader = document.getElementById("file-uploader");
file = "";
url = "";
let msg = "";
fileUploader.addEventListener('change', function () {
    file = this.files;
    // отправляем файл на сохранение в бек
    //если ответ от бека положительный
    id = 2;//из бд должно браться допустим
    //вызываем функцию которая отрисовывает новый блок файла, данные: имя и может номер(id) для удаления из бд
    add_file(file[0].name, id);
});
function back_orders() {
    window.location.href="/profile/";
}
function open_chat() {
    console.log("open_chat");
}

nameOrderp = document.getElementById("name");
statusOrderp = document.getElementById("status");
dateOrderp = document.getElementById("date");
descriptionOrderp = document.getElementById("description");
nameOrderi = document.getElementById("name-i");
statusOrderi = document.getElementById("status-i");
dateOrderi = document.getElementById("date-i");
descriptionOrderi = document.getElementById("description-i");

function change_information() {
    nameOrderp.classList.add("hide");
    statusOrderp.classList.add("hide");
    dateOrderp.classList.add("hide");
    descriptionOrderp.classList.add("hide");
    nameOrderi.classList.remove("hide");
    statusOrderi.classList.remove("hide");
    dateOrderi.classList.remove("hide");
    descriptionOrderi.classList.remove("hide");
    document.getElementById("save-information").classList.remove("hide");
}
function save_information() {
    console.log(200000);
    //отправляем в бек данные: nameOrderi.value, statusOrderi.value, dateOrderi.value, descriptionOrderi.value,
    $.ajax({
                        url: '/editinformationorder/',
                        type: 'POST',
                        data: {
                            name: nameOrderi.value,
//                            description: descriptionOrderi.value,
//                            date: dateline,
//                            time: timeline,
//                            urls: urls,
//                            cloudurls: cloudurlval
                        },
                        dataType: 'json',
                        success: function(data) {
                            alert("Success")
                        },
                        error: function(xhr, textStatus, errorThrown) {
                            alert('Ошибка подключения');
                        }
                    });
    //если сохранилось то идем дальше
    nameOrderp.innerHTML = nameOrderi.value;
    statusOrderp.innerHTML = statusOrderi.value;
    dateOrderp.innerHTML = dateOrderi.value;
    descriptionOrderp.innerHTML = descriptionOrderi.value;
    nameOrderp.classList.remove("hide");
    statusOrderp.classList.remove("hide");
    dateOrderp.classList.remove("hide");
    descriptionOrderp.classList.remove("hide");
    nameOrderi.classList.add("hide");
    statusOrderi.classList.add("hide");
    dateOrderi.classList.add("hide");
    descriptionOrderi.classList.add("hide");
    document.getElementById("save-information").classList.add("hide");
}

function change_files() {
    document.getElementById("save-files").classList.remove("hide");
    document.getElementById("add-file").classList.remove("hide");
    //здесь могут возникнуть проблемы с show/hide кнопки удаления файлы
    // для кнопок удаления чтоб показывались
    countFiles = 3;//количество файлов закинутых в бд/отрисовано блоков файлов
    for (idFile = 1; idFile <= countFiles; idFile++) {
        console.log(idFile);
        document.getElementById(`file-but-sub-${idFile}`).classList.remove("hide");
    }
}
function save_files() {
    //отправляем в бек данные, если сохранилось то идем дальше
    document.getElementById("save-files").classList.add("hide");
    document.getElementById("add-file").classList.add("hide");
    //здесь могут возникнуть проблемы с show/hide кнопки удаления файлы
    // для кнопок удаления чтоб скрывались
    countFiles = 3;//количество файлов закинутых в бд/отрисовано блоков файлов
    for (idFile = 1; idFile <= countFiles; idFile++) {
        console.log(idFile);
        document.getElementById(`file-but-sub-${idFile}`).classList.add("hide");
    }
}
function change_links() {
    document.getElementById("save-links").classList.remove("hide");
    document.getElementById("add-link").classList.remove("hide");
    document.getElementById("input-link").classList.remove("hide");
    //здесь могут возникнуть проблемы с show/hide кнопки удаления ссылки
    // для кнопок удаления чтоб показывались
    // countFiles = 3;//количество ссылок закинутых в бд/отрисовано блоков ссылок
    // for (idFile = 1; idFile <= countFiles; idFile++) {
    //     console.log(idFile);
    //     document.getElementById(`link-but-sub-${idFile}`).classList.remove("hide");
    // }
}
function save_links() {
    //отправляем в бек данные, если сохранилось то идем дальше
    document.getElementById("save-links").classList.add("hide");
    document.getElementById("add-link").classList.add("hide");
    document.getElementById("input-link").classList.add("hide");
    //здесь могут возникнуть проблемы с show/hide кнопки удаления ссылки
    // для кнопок удаления чтоб скрывались
    countFiles = 3;//количество ссылок закинутых в бд/отрисовано блоков ссылок
    for (idFile = 1; idFile <= countFiles; idFile++) {
        console.log(idFile);
        document.getElementById(`link-but-sub-${idFile}`).classList.add("hide");
    }
}
function add_file(nameFile, idFile) {
    const d = document.createElement('div');
    d.setAttribute('class', 'file');
    const p = document.createElement('p');
    p.textContent = nameFile.toString();
    const b = document.createElement('button');
    b.setAttribute('id', `file-but-sub-${idFile}`); // для нумерации и отличия блоков с файлами
    b.textContent = '-';
    const f = document.getElementsByClassName("files")[0];
    f.insertBefore(d, f.lastElementChild);
    d.appendChild(p);
    d.appendChild(b);
    b.addEventListener('click', () => {
        f.removeChild(d);
    });
}
function add_link(){
    const i = document.getElementById("input-link");
    if(i.value=="") {
        console.log("sorry, error");
        return;
    }
    numberLink = 2; //номер ссылки откуда-то подтягивается
    const d = document.createElement('div');
    d.setAttribute('class', 'file');
    const p = document.createElement('p');
    p.textContent = i.value;
    i.value = "";
    const b = document.createElement('button');
    b.setAttribute('id', `link-but-sub-${numberLink}`); // для нумерации и отличия блоков с ссылками
    b.textContent = '-';
    const f = document.getElementsByClassName("links")[0];
    f.insertBefore(d, f.lastElementChild.previousElementSibling);
    d.appendChild(p);
    d.appendChild(b);
    b.addEventListener('click', () => {
        f.removeChild(d);
    });
}

function delete_fileorlink(i, ftype) {
    document.getElementById(`${ftype}-but-sub-${i}`).parentNode.remove();
}