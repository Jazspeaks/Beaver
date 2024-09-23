document.addEventListener('DOMContentLoaded', function () {
    // Function to add a new entry
    function addEntry(section) {
        let sectionDiv = document.getElementById(section);
        let totalFields = sectionDiv.querySelectorAll('.entry-group').length;
        let existingField = sectionDiv.querySelector('.entry-group');
        
        if (totalFields < 20 && existingField) {
            let newField = existingField.cloneNode(true);
            newField.querySelector('input').value = ''; // Clear the value
            
            // Update the name attribute to ensure it's unique
            newField.querySelector('input').name = section + '[]';
            
            sectionDiv.appendChild(newField);
        } else {
            alert("You can only add up to 20 entries or no existing fields to clone.");
        }
    }

    // Function to remove an entry
    function removeEntry(section) {
        let sectionDiv = document.getElementById(section);
        let totalFields = sectionDiv.querySelectorAll('.entry-group').length;

        if (totalFields > 1) {
            sectionDiv.removeChild(sectionDiv.lastChild);
        }
    }

    // Event listeners for buttons
    document.querySelectorAll('.add-field').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            addEntry(button.dataset.section);
        });
    });

    document.querySelectorAll('.remove-field').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            removeEntry(button.dataset.section);
        });
    });
}); // Closing bracket for DOMContentLoaded