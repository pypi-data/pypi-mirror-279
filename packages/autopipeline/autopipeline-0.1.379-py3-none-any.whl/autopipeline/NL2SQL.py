from .util import num_tokens_from_messages
import autopipeline

def query_gen(user_query, tables, description, status, verbose, client, gpt4):
    messages = [
        {
            "role": "system",
            "content": 
            '''
            "Given a database with the following tables: ''' + tables 
            + '''. The detailed descriptions of the tables are as follows: ''' + description
            +
            '''Your task is to generate SQL code that 
            1. can be executed directly on the database in .sqlite format based on users' queries;
            2. the code should produce correct results based on the SAMPLE VALUES AND DESCRPITIONS of each column.''' + '''
            ATTENTION: the values are case-sensitive, and you should strictly follow their provided formats and sample values (if any).
            The code can be of multiple lines, BUT the final assignment has to be assigned to res;
            IMPORTANT: Return the PLAIN code snippets ONLY (DONOT output formatting stuffs like ```sql). You are not allowed to output anything else. 
            '''

        },
        {
            "role": "user",
            "content": '''Name movie titles released in year 1945. Sort the listing by the descending order of movie popularity. Specifically, released in the year 1945 refers to movie_release_year = 1945; 'table \'lists_users\' contains the following columns: column \'user_id\' contains ID related to the user who created the list. with data format being integer and value descriptions being nan; column \'list_id\' contains ID of the list on Mubi with data format being integer and value descriptions being nan; column \'list_update_date_utc\' contains Last update date for the list with data format being text and value descriptions being YYYY-MM-DD; column \'list_creation_date_utc\' contains Creation date for the list with data format being text and value descriptions being YYYY-MM-DD; column \'user_trialist\' contains whether the user was a tralist when he created the list  with data format being integer and value descriptions being 1 = the user was a trialist when he created the list\n 0 = the user was not a trialist when he created the list; column \'user_subscriber\' contains whether the user was a subscriber when he created the list  with data format being integer and value descriptions being 1 = the user was a subscriber when he created the list \n0 = the user was not a subscriber when he created the list; column \'user_avatar_image_url\' contains User profile image URL on Mubi with data format being text and value descriptions being nan; column \'user_cover_image_url\' contains User profile cover image URL on Mubi with data format being text and value descriptions being nan; column \'user_eligible_for_trial\' contains whether the user was eligible for trial when he created the list  with data format being text and value descriptions being 1 = the user was eligible for trial when he created the list \n0 = the user was not eligible for trial when he created the list; column \'user_has_payment_method \' contains whether the user was a paying subscriber when he created the list  with data format being text and value descriptions being 1 = the user was a paying subscriber when he created the list \n0 = the user was not a paying subscriber when he created the list ; table \'lists\' contains the following columns: column \'user_id\' contains ID related to the user who created the list. with data format being integer and value descriptions being nan; column \'list_id\' contains ID of the list on Mubi with data format being integer and value descriptions being nan; column \'list_title\' contains Name of the list with data format being text and value descriptions being nan; column \'list_movie_number\' contains Number of movies added to the list with data format being integer and value descriptions being nan; column \'list_update_timestamp_utc\' contains Last update timestamp for the list with data format being text and value descriptions being nan; column \'list_creation_timestamp_utc\' contains Creation timestamp for the list with data format being text and value descriptions being nan; column \'list_followers\' contains Number of followers on the list with data format being integer and value descriptions being nan; column \'list_url\' contains URL to the list page on Mubi with data format being text and value descriptions being nan; column \'list_comments\' contains Number of comments on the list with data format being integer and value descriptions being nan; column \'list_description\' contains List description made by the user with data format being text and value descriptions being nan; column \'list_cover_image_url\' contains nan with data format being nan and value descriptions being nan; column \'list_first_image_url\' contains nan with data format being nan and value descriptions being nan; column \'list_second_image_url\' contains nan with data format being nan and value descriptions being nan; column \'list_third_image_url\' contains nan with data format being nan and value descriptions being nan; table \'ratings\' contains the following columns: column \'movie_id\' contains Movie ID related to the rating with data format being integer and value descriptions being nan; column \'rating_id\' contains Rating ID on Mubi with data format being integer and value descriptions being nan; column \'rating_url\' contains URL to the rating on Mubi with data format being text and value descriptions being nan; column \'rating_score\' contains Rating score ranging from 1 (lowest) to 5 (highest) with data format being integer and value descriptions being commonsense evidence:\nThe score is proportional to the user\'s liking.\nThe higher the score is, the more the user likes the movie; column \'rating_timestamp_utc \' contains Timestamp for the movie rating made by the user on Mubi with data format being text and value descriptions being nan; column \'critic\' contains Critic made by the user rating the movie.  with data format being text and value descriptions being If value = "None", the user did not write a critic when rating the movie.; column \'critic_likes\' contains Number of likes related to the critic made by the user rating the movie with data format being integer and value descriptions being nan; column \'critic_comments\' contains Number of comments related to the critic made by the user rating the movie with data format being integer and value descriptions being nan; column \'user_id\' contains ID related to the user rating the movie with data format being integer and value descriptions being nan; column \'user_trialist \' contains whether user was a tralist when he rated the movie with data format being integer and value descriptions being 1 = the user was a trialist when he rated the movie \n0 = the user was not a trialist when he rated the movie; column \'user_subscriber\' contains nan with data format being integer and value descriptions being nan; column \'user_eligible_for_trial\' contains nan with data format being integer and value descriptions being nan; column \'user_has_payment_method\' contains nan with data format being integer and value descriptions being nan; table \'ratings_users\' contains the following columns: column \'user_id\' contains ID related to the user rating the movie with data format being integer and value descriptions being nan; column \'rating_date_utc\' contains Rating date for the movie rating. with data format being text and value descriptions being YYYY-MM-DD; column \'user_trialist\' contains whether the user was a trialist when he rated the movie with data format being integer and value descriptions being 1 = the user was a trialist when he rated the movie\n 0 = the user was not a trialist when he rated the movie; column \'user_subscriber\' contains whether the user was a subscriber when he rated the movie with data format being integer and value descriptions being 1 = the user was a subscriber when he rated the movie \n0 = the user was not a subscriber when he rated the movie; column \'user_avatar_image_url\' contains URL to the user profile image on Mubi with data format being text and value descriptions being nan; column \'user_cover_image_url\' contains URL to the user profile cover image on Mubi with data format being text and value descriptions being nan; column \'user_eligible_for_trial\' contains whether the user was eligible for trial when he rated the movie with data format being integer and value descriptions being 1 = the user was eligible for trial when he rated the movie\n 0 = the user was not eligible for trial when he rated the movie; column \'user_has_payment_method \' contains whether the user was a paying subscriber when he rated the movie with data format being integer and value descriptions being 1 = the user was a paying subscriber when he rated the movie \n0 = the user was not a paying subscriber when he rated; table \'movies\' contains the following columns: column \'movie_id\' contains ID related to the movie on Mubi with data format being integer and value descriptions being nan; column \'movie_title\' contains Name of the movie with data format being text and value descriptions being nan; column \'movie_release_year\' contains Release year of the movie with data format being integer and value descriptions being nan; column \'movie_url\' contains URL to the movie page on Mubi with data format being text and value descriptions being nan; column \'movie_title_language\' contains By default, the title is in English. with data format being text and value descriptions being Only contains one value which is \'en\'; column \'movie_popularity\' contains Number of Mubi users who love this movie with data format being integer and value descriptions being nan; column \'movie_image_url\' contains Image URL to the movie on Mubi with data format being text and value descriptions being nan; column \'director_id\' contains ID related to the movie director on Mubi with data format being text and value descriptions being nan; column \'director_name\' contains Full Name of the movie director with data format being text and value descriptions being nan; column \'director_url \' contains URL to the movie director page on Mubi with data format being text and value descriptions being nan; '''
        },
        {
            "role": "assistant",
            "content": "SELECT movie_title FROM movies WHERE movie_release_year = 1945 ORDER BY movie_popularity DESC LIMIT 1",
        },
        {
            "role": "user",
            "content": user_query  # Use the user's query
        }
    ]

    if gpt4:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        if verbose:
            # num_token_msg = num_tokens_from_messages(messages, "gpt-4-0613")
            # print("Number of tokens of messages for 'query_pd': ", num_token_msg)
            print("VERBOSE:"+"Number of prompt tokens for 'query_gen': ", response.usage.prompt_tokens)
            print("VERBOSE:"+"Number of answer tokens for 'query_gen': ", response.usage.completion_tokens)
            print("VERBOSE:"+"Number of total tokens for 'query_gen': ", response.usage.total_tokens)
            current_pize = 0.000005 * response.usage.prompt_tokens + 0.000015 * response.usage.completion_tokens
            print("VERBOSE:"+f"Cost for 'query_gen': ${current_pize}")
            autopipeline.cost += current_pize
            print("VERBOSE:"+f"Accumulated cost: ${autopipeline.cost}")
    else:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages
        )
        if verbose:
            # num_token_msg = num_tokens_from_messages(messages, "gpt-3.5-turbo-0125")
            # print("Number of tokens of messages for 'query_pd': ", num_token_msg)
            print("VERBOSE:"+"Number of prompt tokens for 'query_gen': ", response.usage.prompt_tokens)
            print("VERBOSE:"+"Number of answer tokens for 'query_gen': ", response.usage.completion_tokens)
            print("VERBOSE:"+"Number of total tokens for 'query_gen': ", response.usage.total_tokens)
            current_pize = 0.0000005 * response.usage.prompt_tokens + 0.0000015 * response.usage.completion_tokens
            print("VERBOSE:"+f"Cost for 'query_gen': ${current_pize}")
            autopipeline.cost += current_pize
            print("VERBOSE:"+f"Accumulated cost: ${autopipeline.cost}")
    status.append('code generated')

    if verbose:  # for demo purposes
        content = response.choices[0].message.content
        lines = content.split('\n')
        prefixed_content = '\n'.join('CODE:' + line for line in lines if line.strip())
        print(prefixed_content)
    return response.choices[0].message.content, status