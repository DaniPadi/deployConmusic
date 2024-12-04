document.addEventListener('DOMContentLoaded', () => {
    const selectedStructureInput = document.getElementById('selectedStructure');
    const structureButtons = document.querySelectorAll('.structure-button');
    const removeLastButton = document.getElementById('removeLast');

    structureButtons.forEach(button => {
        button.addEventListener('click', () => {
            const value = button.value;
            
            // Obtener valores actuales y añadir el nuevo valor
            let currentValues = selectedStructureInput.value.split(',').filter(v => v.trim() !== "");
            
            // Añadir el valor seleccionado, permitiendo duplicados
            currentValues.push(value);

            // Actualizar el campo de texto con los valores seleccionados, separados por comas
            selectedStructureInput.value = currentValues.join(',');
        });
    });
    removeLastButton.addEventListener('click', () => {
        // Obtener valores actuales
        let currentValues = selectedStructureInput.value.split(',').map(v => v.trim()).filter(v => v !== "");

        // Eliminar el último valor si hay alguno
        if (currentValues.length > 0) {
            currentValues.pop(); // Elimina el último elemento
        }

        // Actualizar el campo de texto con los valores restantes
        selectedStructureInput.value = currentValues.join(',');
    });
});

document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault();  // Evitar el envío tradicional

    let formData = new FormData(this);

    fetch("/auth/register", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())  // Suponiendo que la respuesta sea JSON
    .then(data => {
        if (data.error) {
            alert(data.error);  // Muestra el error
        } else if (data.message) {
            alert(data.message);  // Muestra el mensaje de éxito
        }
    })
    .catch(error => console.error('Error:', error));
});
