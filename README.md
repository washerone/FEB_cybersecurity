LINK: 
https://github.com/washerone/FEB_cybersecurity/tree/main

This task is updated based on teacher’s advices in 12.2024, also adding the readme file since the essay can not be modified anymore.
As suggested, for flaw 2 the wrong code is commented out, the fixed code is running to ensure the program functions correctly.

Updated again in 04.2025, modifying flaw 3 CSRF

FLAW 1: 
Sensitive Data Exposure
https://github.com/washerone/FEB_cybersecurity/blob/main/flaw/myapp/views.py#L37
Description:
This web application is used to display product information, such as smartphones, laptops.

In the views.py starting from line 33, the current page did not handle the case that user fails to log in securely. If the username or password is wrong, the system may return a detailed error message, such as “Username incorrect”. However, attackers are always able to use such error messages to gather information about the backend system. Without proper security measures, attackers may repeatedly submit incorrect usernames and password attempts to test the system's response, the attackers may find some clues by different combinations of submission. Then attackers get some sensitive information, such as if there exist certain usernames, like “root” and “user” that are often used during development. This flaw will decrease the security of the system. 

How to fix it:
We can handle login failures with a unified error message to avoid leaking sensitive error information. This prevents attackers from “learning” with the error message as their learning material, and as a result reduces the risk of information exposure. In Django, custom the error login view can be implemented to ensure error messages do not reveal sensitive information.


FLAW 2: 
Injection
https://github.com/washerone/FEB_cybersecurity/blob/main/flaw/myapp/views.py#L20

Description: This login form on the page directly passes user input to the database for querying. If not enough preventive mechanisms are adopted, the attackers can insert unsafe SQL code into the username and password parts to skip authentication or execute any SQL queries they want. This will lead to data being exposed or modified. This issue usually is caused by not using processed statements or ORM (Object-Relational Mapping) queries in Django.

Fix: using ORM for procesing database queries. In Django, its ORM automatically parameterizes all the queries, preventing SQL injection attacks. Moreover, we can use authenticate () in Django, to make the code safer and clearer (no “except” structure needed).

Please note that this flaw is already fixed, as I explained in the code, due to the function here is connected with other parts, a fixed code here can make sure the other functions and flaws demonstrated clearly.


FLAW 3:
CSRF
https://github.com/washerone/FEB_cybersecurity/blob/main/flaw/templates/login.html#L92

Flaw 3 description: If the form modifies user data such as login or updating information, it should include the {% csrf_token %} tag to prevent CSRF attacks. However, in this code the {% csrf_token %} tag has been commented out, so the form submission does not automatically include CSRF token. Moreover, the backend view function is marked with @csrf_exempt, which disables CSRF protection.

This could lead to a CSRF attack, attackers can forge requests and tricks users into performing unintended actions, such as modifying user profiles or submitting forms.

Fix:
We should ensure that every form that submits user data includes the {% csrf_token %} tag. To fix the issue, add {% csrf_token %} into the form so that Django can generates and includes a CSRF token. And in views.py, we should remove the @csrf_exempt from the login() function.


FLAW 4:
Cross-Site Scripting (XSS)
https://github.com/washerone/FEB_cybersecurity/blob/main/flaw/templates/dashboard.html#L106

Description:
In the dashboard.html:
<h3 class="product-name">{{ product.name|safe }}</h3>
<p class="product-description">{{ product.description|safe }}</p >
<p class="product-price">{{ product.price }}</p >

The product description is displayed directly on the webpage without any filtering or escaping. If a user input contains malicious JavaScript code in the product description, other users viewing the product may unknowingly execute these scripts, leading to a Cross-Site Scripting attack.

Fix:
In order to prevent XSS attacks, we need to escape user inputs. In Django templates, output will be automatically escaped, but if raw HTML insertion is required, we should explicitly use the escape filter to handle the input securely.

In the dashboard.html, I use Django built-in escape filter to escape user inputs and make sure no malicious scripts can be executed.


FLAW 5:
Broken Access Control
https://github.com/washerone/FEB_cybersecurity/blob/main/flaw/templates/dashboard.html#L122

Description:
The product prices are displayed directly on the webpage, all the user that browse the webpage can see it. But in fact, displaying certain product prices requires some authentication, for example product only for membership or a special offer. The flaw here results in unauthenticated users have access to restricted data.

Fix:
We can dynamically manage the displayed price based on user permissions to fix it. The webpage should display member exclusive prices only to authenticated members. For users who are not authenticated, the webpage can either hide the price or display a notice message.

Hence, in the fixing code in dashboard.html, we can add a variable, to control the access to the product price. The added variable can indicate whether the price is visible based on user permissions.


FLAW 6:
Insecure Deserialization 
https://github.com/washerone/FEB_cybersecurity/blob/main/flaw/myapp/views.py#L69

Flaw 6 description:
In the load_data view, the server directly deserializes the data that user submits. Specifically, pickle.loads(data) directly deserializes the submitted data, without any verification. This practice is highly insecure because pickle can allow any object deserialization, which may lead to executing the __reduce__ method to any objects during the process, resulting in unknown code to be executed. The attackers can craft malicious pickled data and submit it, result in the vulnerability to execute unauthorized commands or expose sensitive data.

Fix:
We should avoid insecure deserialization libraries like pickle for the submitted data. 
In the fix I use deserialization with json, as deserialized objects in json only support simple data types and do not execute unknown code during deserialization. Hence, we should 
replace pickle.loads() with json.loads(), which is significantly safer and reduce the risk of executing malicious code.
