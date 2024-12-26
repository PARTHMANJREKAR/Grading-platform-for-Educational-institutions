function updateContent(newContent) {
    document.getElementById('content').innerHTML = newContent;
}

function openSelectSubject() {
    const subjectsHTML = `
        <h1>Select Subject</h1>
        <div class="buttons">
            <a href="javascript:void(0)" class="square-button" ondblclick="selectEvaluationType()">SUBJECT 1</a>
            <a href="javascript:void(0)" class="square-button" ondblclick="selectEvaluationType()">SUBJECT 2</a>
            <a href="javascript:void(0)" class="square-button" ondblclick="selectEvaluationType()">SUBJECT 3</a>
            <a href="javascript:void(0)" class="square-button" ondblclick="selectEvaluationType()">SUBJECT 4</a>
            <a href="javascript:void(0)" class="square-button" ondblclick="selectEvaluationType()">SUBJECT 5</a>
            <a href="javascript:void(0)" class="square-button" ondblclick="selectEvaluationType()">SUBJECT 6</a>
        </div>
    `;
    updateContent(subjectsHTML);
}

function selectEvaluationType() {
    const evaluationTypes = ["THEORY", "PRACTICAL"];
    const evaluationOptions = evaluationTypes.map(type => `
        <a href="javascript:void(0)" class="square-button" ondblclick="selectSubject('${type}')">${type}</a>
    `).join("");

    updateContent(`
        <h1>Select Evaluation Type</h1>
        <div class="buttons">${evaluationOptions}</div>
    `);
}

function selectSubject(type) {
    const evaluationTypes = ["CCE", "ESE", "Attendance"];
    const evaluationOptions = evaluationTypes.map(evaluationType => `
        <a href="javascript:void(0)" class="square-button" ondblclick="showInputForm('${type}', '${evaluationType}', 0)">${evaluationType}</a>
    `).join("");

    updateContent(`
        <h1>Select Evaluation Type for ${type}</h1>
        <div class="buttons">${evaluationOptions}</div>
    `);
}

function showInputForm(type, evaluationType, studentIndex) {
    const rollNumbers = Array.from({ length: 70 }, (_, i) => `Roll Number ${i + 1}`);

    function renderCIAInputGroups() {
        const groups = [
            { title: "Group 1", inputs: 6 },
            { title: "Group 2", inputs: 4 },
            { title: "Group 3", inputs: 5 },
            { title: "Group 4", inputs: 2 },
            { title: "Group 5", inputs: 6 },
            { title: "Group 6", inputs: 5 },
            { title: "Group 7", inputs: 5 },
        ];

        return groups.map((group, index) => `
            <div class="group-box">
                <div class="group-title">
                    ${group.title} <input type="checkbox" class="group-checkbox" id="group-${index}" onchange="handleGroupSelection(${index})">
                </div>
                <div class="input-group">
                    ${Array.from({ length: group.inputs }, (_, i) => `
                        <label for="input-${index}-${i}">Input ${i + 1}:</label>
                        <input type="number" id="input-${index}-${i}" name="input-${index}-${i}" class="input-field" min="0" max="10" required>
                    `).join('')}
                </div>
            </div>
        `).join('');
    }

    function renderOtherInputs(type) {
        switch (type) {
            case "ESE":
                return `
                    <label for="ese-input">ESE Input:</label>
                    <input type="number" id="ese-input" name="ese-input" min="0" max="10" required>
                `;
            case "Attendance":
                return `
                    <label for="attendance-input">Attendance Input:</label>
                    <input type="number" id="attendance-input" name="attendance-input" min="0" max="100" required>
                `;
            default:
                return '';
        }
    }

    updateContent(`
        <h1>Enter Details for ${evaluationType} - ${type} (Student ${studentIndex + 1})</h1>
        <div id="student-roll-display">Roll Number: ${rollNumbers[studentIndex]}</div>
        <select id="student-select" onchange="jumpToStudent('${type}', '${evaluationType}')">
            ${rollNumbers.map((roll, index) => `
                <option value="${index}" ${index === studentIndex ? 'selected' : ''}>${roll}</option>
            `).join('')}
        </select>
        <form id="input-form">
            ${evaluationType === "CCE" ? renderCIAInputGroups() : renderOtherInputs(evaluationType)}
            <button type="button" onclick="saveStudentData('${type}', '${evaluationType}', ${studentIndex})">
                ${studentIndex < 69 ? 'Next Student' : 'Save & Export'}
            </button>
        </form>
    `);
    attachInputValidation();
}

function handleGroupSelection(groupIndex) {
    const checkbox = document.getElementById(`group-${groupIndex}`);
    if (checkbox.checked) {
        if (selectedGroups.length >= maxSelectableGroups) {
            alert("You can select a maximum of 2 groups.");
            checkbox.checked = false;
        } else {
            selectedGroups.push(groupIndex);
        }
    } else {
        selectedGroups = selectedGroups.filter(index => index !== groupIndex);
    }
}

function attachGroupSelectionHandlers() {
    const checkboxes = document.querySelectorAll(".group-checkbox");
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            const groupIndex = parseInt(checkbox.id.replace('group-', ''), 10);
            handleGroupSelection(groupIndex);
        });
    });
}

function attachInputValidation() {
    const inputs = document.querySelectorAll(".input-field");
    inputs.forEach(input => {
        input.addEventListener("input", (event) => {
            const value = event.target.value;
            if (value < 0 || value > 10) {
                event.target.setCustomValidity("Value must be between 0 and 10.");
            } else {
                event.target.setCustomValidity("");
            }
        });
    });
}

function jumpToStudent(type, evaluationType) {
    const studentIndex = parseInt(document.getElementById("student-select").value, 10);
    showInputForm(type, evaluationType, studentIndex);
}

function saveStudentData(type, evaluationType, studentIndex) {
    const formData = new FormData(document.getElementById("input-form"));
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    console.log(`Saving data for ${type} - ${evaluationType} - Student ${studentIndex + 1}:`, data);

    if (studentIndex < 69) {
        showInputForm(type, evaluationType, studentIndex + 1);
    } else {
        alert("All data saved. You can now export the results.");
        // Implement the export functionality here
    }
}
