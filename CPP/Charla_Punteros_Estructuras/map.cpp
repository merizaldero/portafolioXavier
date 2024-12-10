#include <iostream>
#include <map>
using namespace std;

void imprimir_map(map<string, int> a){
    cout << "Tamaño Map " << a.size() << "\n";    
    if(! a.empty()){
        for(auto clave_valor : a){
            cout << clave_valor.first << " : " << clave_valor.second << "\n" ;
        }
    }
    cout << "\n";
}

int main(){
    map<string, int> edades = { {"Pedro", 15}, {"Pablo", 13}, {"Juan", 20} };
    imprimir_map(edades);

    edades.insert( {"Cristina", 22} );
    edades.insert( {"Pablo", 15} );
    edades["Andres"] = 27;
    imprimir_map(edades);

    edades.erase("Juan");
    imprimir_map(edades);

    return 0;
}