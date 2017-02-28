"use strict";

function insertDiv(result, container) {

    var ingredients = "";
    // console.log(result["ingredients"]);
    for (var ingredient of result["ingredients"]) {
        // console.log(ingredient);
        // var newIngred;
        if (ingredient["unit"] != null) {
            var newIngred = "<p>" + ingredient["quantity"] + " " + ingredient["unit"] + " " + ingredient["ingredient_name"] + "</p>";
            // console.log(newIngred);
            } else {
                newIngred = "<p>" + ingredient["quantity"] + " " + ingredient["ingredient_name"] + "</p>";
            }
            // console.log(newIngred);
        ingredients += newIngred;
        }
    // var steps = "Instructions " + result["steps"];
    // ingredients.append(instructions)
    container.append("<div>" + ingredients + "</div>");
    // container.append("<div>" + steps + "</div>");
}

function showHashRecipes(results) {
    for (var hashtag in results) {
        var container = $("#" + results[hashtag]["hashtag_id"]);
        for (var recipe of results[hashtag]["recipes"]) {
            var formInput = {
                "recipe_id": recipe[0],
                "container_id": container.value
                };
// TODO: look into how to make a synchronous ajax request - I'm getting a console log warning about this one 
            $.ajax({
                  type: 'POST',
                  url: "/view_recipe.json",
                  data: formInput,
                  success: function(results) {
                    // console.log(container);
                    insertDiv(results, container);
                    },
                  async:false
                });
        }
        //     $.post("/view_recipe.json", formInput, function(results) {
        //         console.log(container);
        //         insertDiv(results, container);
        //     });
        // }
    }

}

$.get('/display_hashed_recipes.json', showHashRecipes);

function showRecipe(result) {
    var recipe_id = result["recipe_id"];
    $('#summary-' + recipe_id).empty();
    if ($('.userid').length != 0) {
        if (result["is_starring"] === "false") {
                // $('#div-' + recipe_id).append("<button type='button' data-id=" + recipe_id + " class='starButton'>Star this recipe!</button>")
            $('*[data-id='+recipe_id+"]").toggle();
            }
        if (result["is_starring"] === "true") {
            $('#div-' + recipe_id).append("<p>You've starred this recipe</p>")
        }
    }
    if (typeof result["time"] != "undefined") {
        $('#' + recipe_id).innerText.append("<span>" + result["time"] + " minutes</span>");
    }  
    for (var ingredient of result["ingredients"]) {
        if (ingredient["unit"] != null) {
            $('#ingredients-' + recipe_id).append("<p>" + ingredient["quantity"] + " " + ingredient["unit"] + " " + ingredient["ingredient_name"] + "</p>");
            } else {
                $('#ingredients-' + recipe_id).append("<p>" + ingredient["quantity"] + " " + ingredient["ingredient_name"] + "</p>");
            }
        }
    $('#instructions-' + recipe_id).append(result["steps"]);
}

$('.starButton').on('click', starRecipe);

function getRecipeInfo(evt) {
    var recipe_id = $(this).attr('id');
    var formInput = {
        "recipe_id": recipe_id
    };
    $.post("/view_recipe.json", formInput, showRecipe);
}

$('.recipe_name').on('click', getRecipeInfo);

function starRecipe() {
    // evt.preventDefault();
    console.log("You have starred the recipe");
    var recipe_id = $( this ).data('id');

    // console.log(recipe_id);
    var formInput = {
        "recipe_id": recipe_id
    };

    $.post("/star_recipe.json", formInput, console.log("recipe starred"));
    $('*[data-id='+recipe_id+"]").toggle();
}

function addHashtag() {
    var recipe_id = $( this ).data('id');
    var hashtag_name = $("input[name=hashtag-" + recipe_id + "]").val()
    var formInput = {
        "recipe_id": recipe_id,
        "hashtag_name": hashtag_name
    };
    $.post("/add_hashtag.json", formInput, populateHash);
}

function populateHash(results) {
    // console.log("populating the hash")
    var recipe_id = results["recipe_id"];
    $('#hashtags-' + recipe_id).append(results['hashtag_name'] + " ");
    $('#del-hashtag-' + recipe_id).append("<option value=" + results['hashtag_name'] + ">" + results['hashtag_name'] + "</option>")
}

$('.submit-button').on('click', addHashtag);

function delHashtagization() {
    var recipe_id = $( this ).data('id');
    var hashtag_name = $('#del-hashtag-' + recipe_id).val();
    // Delete the removed hashtag from the "remove" options
    $('#del-hashtag-' + recipe_id + " option[value=" + hashtag_name + ']').remove();

    var formInput = {
        "recipe_id": recipe_id,
        "hashtag_name": hashtag_name
    };
    $.post("/del_hashtagization.json", formInput, updateDeletedHash);
}

function updateDeletedHash(results) {
    var recipe_id = results["recipe_id"];
    var hashtags = results["hashtags"];
    // empty the div populated with the recipe's hashtags
    $('#hashtags-' + recipe_id).empty();
    // repopulate the div with the updated list of hashtags
    for (var hashtag of hashtags) {
        $('#hashtags-' + recipe_id).append(hashtag);
        $('#hashtags-' + recipe_id).append(" ");
    }
}
$('.del_hashtag').on('click', delHashtagization);




// function showHashtags() {
//     if ($('.userid').length != 0)
// }
//         function () {
//         recipe_id = formInput.recipe_id
//         $('[data-id=recipe_id]').innerHtml("Recipe starred");
//     }
//     );
// }


