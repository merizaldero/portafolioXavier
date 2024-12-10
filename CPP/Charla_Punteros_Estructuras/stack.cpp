#include <iostream>
#include <stack>
using namespace std;

void evaluar_pila(stack<string> pila){
    cout << "Conteo de Pila: " << pila.size() << "\n"; 
    if(!pila.empty()){
        cout << "Top Actual: " << pila.top() << "\n";
    }
    cout << "\n";
}
int main(){
    stack<string> carros;
    evaluar_pila(carros);

    carros.push("Volvo");
    carros.push("BMW");
    carros.push("Ford");
    evaluar_pila(carros);

    carros.top() = "Andino";
    evaluar_pila(carros);

    carros.pop();
    evaluar_pila(carros);

    while( carros.size() > 0 ){
        carros.pop();
    }
    evaluar_pila(carros);

    return 0;
}