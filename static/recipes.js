"use strict";

// function showHashRecipes(results) {
//     // Iterate through the recipes, and for each recipe...
//     for (var hashtag in results) {
//         var hashrecipes = results[hashtag];
//         for (var recipe_name in hashrecipes) {
//             var recipe = hashrecipes[recipe_name]
//             // ...call showRecipe to display the recipe
//             showRecipe(recipe);
//         }
//     }
// }
// $.get('/user-hashtag-recipes.json', showHashRecipes);


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
        $('#div-' + recipe_id).append("<p>Total time required: " + result["time"] + " minutes</p>");
    }  
    $('#div-' + recipe_id).append("<a name={{ result['id'] }}><p>Ingredients:</p></a>");
    for (var ingredient of result["ingredients"]) {
        if (ingredient["unit"] != null) {
            $('#div-' + recipe_id).append("<p>" + ingredient["quantity"] + " " + ingredient["unit"] + " " + ingredient["ingredient_name"] + "</p>");
            } else {
                $('#div-' + recipe_id).append("<p>" + ingredient["quantity"] + " " + ingredient["ingredient_name"] + "</p>");
            }
        }
    $('#div-' + recipe_id).append("<p>Instructions:</p>");
    $('#div-' + recipe_id).append(result["steps"]);
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
    var recipe_id = results["recipe_id"]
    $('#hashtags-' + recipe_id).append(results['hashtag_name']);
}

$('.submit-button').on('click', addHashtag);

function delHashtagization() {
    var recipe_id = $( this ).data('id');
    var hashtag_name = $("select[name=del_hashtag-" + recipe_id + "]").val()

    var formInput = {
        "recipe_id": recipe_id,
        "hashtag_name": hashtag_name
    };
    $.post("/del_hashtagization.json", formInput, console.log("Hashtag deleted"));
}
$('#del_hashtag').on('click', delHashtagization);

// function showHashtags() {
//     if ($('.userid').length != 0)
// }
//         function () {
//         recipe_id = formInput.recipe_id
//         $('[data-id=recipe_id]').innerHtml("Recipe starred");
//     }
//     );
// }


