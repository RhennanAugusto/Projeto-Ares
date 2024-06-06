function add_ares(){
    container = document.getElementById('form-ares')

    html = "<br><div class='row'> <div class='col-md'> <input type = 'text' placeholder='Ar' class='form-control' name='ar'></div> <div class='col-md'><input type='text' placeholder='Marca' class='form-control' name='marca' ></div> <div class='col-md'> <input type='number' placeholder='Ano de instalação' class='form-control' name='ano'></div> </div>"
    
    container.innerHTML += html 
}

function exibir_form(tipo){
    
    add_clientes = document.getElementById('adicionar-cliente')
    att_clientes = document.getElementById('att_clientes')
    
    if(tipo == "1") {
        att_clientes.style.display = "none" // jeito de manter apenas o form que queremos aparecendo e não os dois ao mesmo tempo
        add_clientes.style.display = "block"
    }else if (tipo == "2"){
        att_clientes.style.display = "block"
        add_clientes.style.display = "none"
    }

}

function dados_cliente(){
    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value
    data = new FormData()
    data.append('id_cliente',id_cliente)
    fetch("/clientes/atualiza_cliente/",{
        method: "POST", 
        headers:{
            'X-CSRFToken': csrf_token,
        },
        body: data 
    
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        document.getElementById('form-att-cliente').style.display = 'block'
   
        id = document.getElementById('id')
        id.value = data['cliente_id'] 
        nome = document.getElementById('nome')
        nome.value = data ['cliente'] ['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data ['cliente'] ['sobrenome']

        cpf = document.getElementById('cpf')
        cpf.value = data ['cliente'] ['cpf']

        email = document.getElementById('email')
        email.value = data ['cliente'] ['email']

        div_ares = document.getElementById('ares')
        div_ares.innerHTML=""
        for(i=0; i<data['ares'].length; i++){
            

            div_ares.innerHTML += "<form action='/clientes/update_ar/"+data['ares'][i]['id']+"' method='POST'>\
               <div class ='row'>\
                   <div class ='col-md'>\
                      <input class='form-control' type='text' name='ar' value='"+ data['ares'][i]['fields']['ar'] +"'>\
                    </div>\
                    <div class ='col-md'>\
                      <input class='form-control' type='text' name='marca' value='"+ data['ares'][i]['fields']['marca'] +"'>\
                    </div>\
                    <div class ='col-md'>\
                      <input class='form-control' type='text' name='ano' value='"+ data['ares'][i]['fields']['ano'] +"'>\
                    </div>\
                    <div class ='col-md'>\
                      <input class='btn btn-success' type='submit' value='Salvar'>\
                    </div>\
                    </form>\
                    <div class ='col-md'>\
                        <a class='btn btn-danger' href='/clientes/excluir_ar/" + data ['ares'][i]['id'] + "'>Excluir</a>\
                    </div>\
               </div><br>"
            
        }
    }) //fetch é uma forma de fazer requisições para uma determinada endpoint de um backend e a response podemos tratar por exemplo com o json
}

function update_cliente(){
    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value
    id = document.getElementById('id').value

    fetch('/clientes/update_cliente/'+ id, {
        method: 'POST',
        headers:{
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({    
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf,
        })
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
       if(data['status']==200){
            
        location.reload();
       }else{
          setErrorFor(input)
       }
           
    })
}