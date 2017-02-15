"use strict";

function showHashRecipes(results){
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

// function showRecipe(results){
//      $('#recipe').append("<h4>" + results["recipe_name"] + "</h4>");
//             $('#recipe').append("<p>Total time required: " + results["time"] + " minutes</p>");
//             $('#recipe').append("<p>Ingredients:</p>");
//             for (var ingredient of results["ingredients"]) {
//                 $('#recipe').append("<p>" + ingredient["quantity"] + " " + ingredient["unit"] + " " + ingredient["ingredient_name"] + "</p>");
//             $('#recipe').append("<p>Instructions:</p>");
//             $('#recipe').append(results["steps"]);
// }

// $.get('/recipe.json', {"recipe_id": recipe.recipe_id}, showRecipe);