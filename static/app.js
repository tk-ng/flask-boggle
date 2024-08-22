const BASE_URL = "http://127.0.0.1:5000";
let score = 0;
let answers = [];

setTimeout(disableField, 60000);

async function disableField() {
	$("button").prop("disabled", true);
	let finalScore = $("#score").text();
	const resp = await axios({
		url: `${BASE_URL}/gameover`,
		method: "POST",
		data: { score: finalScore },
	});
	$("#result p").text("Times Up!");
	console.log(resp.data);
}

$("form").on("submit", async function (evt) {
	evt.preventDefault();
	inputValue = $("input").val();
	if (answers.includes(inputValue)) {
		$("#result p").text("The word has been submitted before");
		return;
	}
	result = await submit(inputValue);
	if (result == "ok") {
		$("#result p").text("Good Job!");
		score += inputValue.length;
		$("#score").text(score);
		answers.push(inputValue);
	} else if (result == "not-word") {
		$("#result p").text("That's not a valid word!");
	} else {
		$("#result p").text("The word is not found on the board!");
	}
});

async function submit(value) {
	const response = await axios({
		url: `${BASE_URL}/validate`,
		method: "POST",
		data: { guess: value },
	});
	const { result } = response.data;
	return result;
}
