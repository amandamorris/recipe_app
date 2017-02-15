"use strict";

function showHashRecipes(results) {
    for (var hashtag in results) {
        var hashrecipes = results[hashtag];
        for (var recipe_name in hashrecipes) {
            var recipe = hashrecipes[recipe_name]
            $('#' + hashtag).append("<h4>" + recipe_name + "</h4>");
            $('#' + hashtag).append("<p>Total time required: " + recipe["time"] + " minutes</p>");
            $('#' + hashtag).append("<p>Ingredients:</p>");
            for (var ingredient of recipe["ingredients"]) {
                $('#' + hashtag).append("<p>" + ingredient["quantity"] + " " + ingredient["unit"] + " " + ingredient["ingredient_name"] + "</p>");
            $('#' + hashtag).append("<p>Instructions:</p>");
            $('#' + hashtag).append(recipe["steps"]);

            }

        }
    }
    
}
$.get('/user-hashtag-recipes.json', showHashRecipes);

function showRecipe(result) {
    var recipe_id = result["recipe_id"];
    $('#div-' + recipe_id).empty();
     $('#div-' + recipe_id).append("<h4>" + result["recipe_name"] + "</h4>");
            $('#div-' + recipe_id).append("<p>Total time required: " + result["time"] + " minutes</p>");
            $('#div-' + recipe_id).append("<p>Ingredients:</p>");
            for (var ingredient of result["ingredients"]) {
                $('#div-' + recipe_id).append("<p>" + ingredient["quantity"] + " " + ingredient["unit"] + " " + ingredient["ingredient_name"] + "</p>");
            }
            $('#div-' + recipe_id).append("<p>Instructions:</p>");
            $('#div-' + recipe_id).append(result["steps"]);
}

// $.get('/recipe.json', {"recipe_id": recipe.recipe_id}, showRecipe);
// When you click on a recipe name, get the id for that recipe, and pass it to
// view_recipe.json, return the jsonified recipe, and on return, call showRecipe
function getRecipeInfo(evt) {
    console.log("you clicked me");
    // console.log($( this ));
    // evt.preventDefault();
    var recipe_id = $( this ).attr('id');
    console.log(recipe_id);
    var formInput = {
        "recipe_id": recipe_id
    };
    $.post("/view_recipe.json", formInput, showRecipe);
}

$('.recipe_name').on('click', getRecipeInfo);
