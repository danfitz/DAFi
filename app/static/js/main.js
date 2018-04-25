function checkLength() {
    goalsList = document.getElementById("childGoals").children;

    return goalsList.length;
}

let count = 1;

function addChildGoal() {
    // Create new goal element, a li
    let goalElement = document.createElement("li");
    goalElement.setAttribute("id", "childGoalNum-" + count);

    // Create label element
    let goalLabel = document.createElement("label");
    goalLabel.setAttribute("for", "childGoals-" + count);
    goalLabel.innerHTML = "Is this your smallest goal?";

    // Create input element
    let goalInput = document.createElement("input");
    goalInput.setAttribute("id", "childGoals-" + count);
    goalInput.setAttribute("name", "childGoals-" + count);
    goalInput.setAttribute("type", "text");
    goalInput.setAttribute("value", "");

    // Create remove button that calls removeGoal() function
    let goalRemover = document.createElement("button");
    goalRemover.setAttribute("type", "button");
    goalRemover.setAttribute("onClick", "removeChildGoal(" + count + ")");
    goalRemover.innerHTML = "Remove";

    // Create br element
    let br = document.createElement("br");

    // Appends label, input, and remove button to li goal element
    goalElement.appendChild(br);
    goalElement.appendChild(br);
    goalElement.appendChild(br);
    goalElement.appendChild(br);
    goalElement.appendChild(goalLabel);
    goalElement.appendChild(br);
    goalElement.appendChild(goalInput);
    goalElement.appendChild(goalRemover);

    // Append li goal element to HTML of page
    let goalsList = document.getElementById("childGoals");
    goalsList.appendChild(goalElement);

    count += 1;
}

function removeChildGoal(count) {
    document.getElementById("childGoalNum-" + count).remove();
}

