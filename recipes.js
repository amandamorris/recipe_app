"use strict";

function showHashRecipes(results){
    // console.log(results);
    for (var hashtag in results) {
        // console.log(hashtag);
        var hashrecipes = results[hashtag];
        for (var recipe_name in hashrecipes) {
            var recipe = hashrecipes[recipe_name]
            console.log(hashtag);
            console.log(recipe_name);
            $('#' + hashtag).append("<h4>" + recipe_name + "</h4>");
            $('#' + hashtag).append("<p>Total time required: " + recipe["time"] + " minutes</p>");
            $('#' + hashtag).append("<p>Ingredients:</p>");
            for (var ingredient of recipe["ingredients"]) {
    //             // console.log(ingredient);
    //             // console.log(ingredient["ingredient_name"]);
                $('#' + hashtag).append("<p>" + ingredient["quantity"] + " " + ingredient["unit"] + " " + ingredient["ingredient_name"] + "</p>");
            $('#' + hashtag).append("<p>Instructions:</p>");
            $('#' + hashtag).append(recipe["steps"]);

            }

        }
    }
    
}

$.get('/user-hashtag-recipes.json', showHashRecipes);

