---
title: "Secure PHP Login"
date: 2012-02-29
tags: 
  - "instructional"
  - "programming"
---

When perusing the internet for discussions on PHP sessions and cookies in regards to credential validation and user logins, I've never been satisfied with the approaches I find. Many of the tutorials are just plain lousy or incomplete. And the others seem to imply that you should only use sessions _or_ cookies and never mix-and-match, a confusion that would probably trip up many PHP novices. So I've decided to post a tutorial explaining the complete PHP login format I use for my sites and web applications. Before we start, I should let you know that you can grab all the source in this tutorial [from GitHub](https://github.com/alexdlaird/secure-php-login).

# How it Works

The way to create secure pages using PHP is a simple enough concept: determine the pages that can only be visited by logged in users and put a piece of code at the top of them to redirect logged out users to a login page. If a user visits the login page and is already logged in, they should be redirected to the main page.

So, how do you determine if a user has been logged in? You have PHP to see if there's a fingerprint that pairs the server to the client's computer. To do this, PHP provides access to two mechanisms: sessions and cookies. Once a user has logged in with a valid username and password, you fingerprint either the server (session) or the client's computer (cookie). Once the fingerprint is in place, each secured page just needs to check to see if it exists. If it does, show the page to the user; if not, kick the user back to the login page.

It's that simple.

# Comparing Sessions and Cookies

Before you can really proceed, you need to understand the primary differences between sessions and cookies in PHP (and, well, anywhere). Let's break them down for comparison:

**Cookie**

- Stored on client's computer
- Slower, since they have to be sent to the server from the client's computer
- Limited on size and how many can be stored on the client's computer
- Can be used across multiple servers
- Can have a lengthy lifespan
- Can be viewed and modified by client and can therefore be a security risk, depending on the content
- Not available until page reloads, since cookies will be sent to the server on page load

**Session**

- Stored on server
- Faster, since they are already on the server
- Less bandwidth transfer since, rather than sending all data from client to server, the session only sends the session ID to be stored in a cookie on the client's computer
- Size of a session is dependent on the PHP memory limit set in php.ini, but my guess is that limit is _significantly_ higher on your server than the 4k generally allotted to cookies
- Cannot be used across multiple servers
- Lifespan is very short; always destroyed when browser has been closed
- Can only be accessed through the server, so much more secure than cookies
- Available immediately in code without a page reload

From the above, you should be able to deduce that if you are working with sensitive data (passwords, credit card data, etc.), a session should be used. If you simply want to carry non-sensitive data between pages (the contents of a shopping cart), a cookie may be used.

Now that we understand the differences between sessions and cookies functionally speaking, what are they? Basically, as far as the code is concerned, they're just arrays. The cookie array can be accessed using _$_COOKIE['project-name']['val-name']_, and the session array is conditionally accessible by referencing _$_SESSION['project-name']['val-name']_. The session array is only accessible if you have started a session by calling _session_start()_.

To store a value into a cookie, we use the provided function _setcookie('project-name[val-name]', $myData, time () + $keepAlive)_. Now let's break this down: _val-name_ will be the string used to reference this cookie as shown in the paragraph above. Whatever is in _$myData_ is the string that will be stored in the cookie, and the cookie will stay alive until _$keepAlive_ seconds from the current time have passed.

To store a value into a session is much easier. After a session has started, you simply execute _$_SESSION['project-name']['val-name'] = $myData_. The values will be accessible as shown above so long as the session exists—that is to say, so long as the browser has not been closed and _session_destory()_ has not been called.

With this understanding of sessions and cookies now, you should be able to see that a session will be useful in allowing a user to login to a secured page, but that it will not allow a user to close the browser and return to that page still logged in. We're just about to dive into the code that will allow for both of those things, but first let's look at a common oversight.

# The Shared Server Conundrum

This is a sneaky issue, because you likely won't know that it exists until your security has been compromised, so I'll let you in on the secret now.

PHP session variables are stored in /tmp by default, and this is true for any user on a server. Since the HTTP server software has access to read and write from this folder, and all users of a shared server execute from that same user, there is never a complete guarantee that your sessions are completely safe when you're in a shared server environment. It is also possible for session collisions to occur because of this, for instance, if you and another user on a shared server are using the same session string. For this reason, it's a good idea to regularly regenerate the session ID, and it's also smart to use session strings that are related to the application you're working with.

Another issue with shared server sessions in PHP is their timeout time. Though you may set a session timeout to be five hours, if another user on the shared server sets the timeout to be something else, say two hours, all of your sessions will also timeout in two hours, since PHP does not disambiguate between users within the /tmp folder.

I don't know of a remedy for the timeout issue, though you may be able to contact your server admin to ask if there is a user-based php.ini file that could be configured to store your sessions somewhere other than /tmp. There are also ways to store your sessions in a database, which would get rid of both of these potential issues.

Regardless, neither of these issues are extreme vulnerabilities, but they should be something you're aware of. If your application simply cannot share its sessions with other users, or your session data needs to be tightly maintained and secured, your best bet is to go with a dedicated server.

# User Database

Before we can make a secured page that only certain users have access to, we need an access list of those users and their credentials, right? The way we achieve that goal is with a database. In our code example below, we're using a MySQL database, so you'll need to perform the following steps using MySQL:

- Create a database named **project_name**
- Create a table within **project_name** named **Users**
- **Users** should have (at least) three columns: **UserID** _int(11)_, **Username** _char(25)_, and **Password** _char(60)_
    - The **UserID** column needs to be unique and auto-incrementing, starting at one (1)—the code below checks for a **UserID** equal to zero, which means that the user was not in the database
    - Ideally, the **UserID** column should be the primary index for the table
- **Users** should have (at least) one row added: plain text **Username**, and hashed **Password**

Once a MySQL database setup like this, you're ready to write the PHP code.

If you are a PHP beginner, please look into database sanitization. Anytime you are going to be accepting input from a web form and passing that input into a database (for example, in the case of accepting user credentials and logging that user into the website), you need to sanitize the inputs to prevent potential attacks on your website. In the source code below, database inputs are sanitized through the use PHP's PDO library.

# The Code

The snippets of PHP code below are robust enough to be deployed with a large-scale web application. If all you require is a simple authentication page and don't much plan on using the session variables throughout your user's stay, this code can easily be trimmed down to fit those needs as well. So, let's walk through the code, shall we?

**class-databasehelpers.php**

If you are making a large-scale web application a database helpers class can help streamline repetitive database calls. If you are making a more simple login interface, you can move the functionality within this class to **functions.php**.

If your application eventually has a **settings.php** file, it'd make more sense to move the defined database constants out there.

```php
php

define ('DB_HOST', 'localhost'); define ('DB_NAME', 'project_name'); define ('DB_USERNAME', 'sql-username'); define ('DB_PASSWORD', 'sql-password');

class DatabaseHelpers { function blowfishCrypt($password, $length) { $chars = './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'; $salt = sprintf ('$2a$%02d$', $length); for ($i=0; $i < 22; $i++) { $salt .= $chars[rand (0,63)]; }

return crypt ($password, $salt); }

public function getDatabaseConnection() { $dbh = new PDO('mysql:host=' . DB_HOST . ';dbname=' . DB_NAME, DB_USERNAME, DB_PASSWORD);

$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

return $dbh; } }

?>
```

**class-userdata.php**

The _UserData_ class should be an almost identical interface to the MySQL **Users** table. _Almost_ identical. You should not have the **Password** field, as PHP will handle checking that value and beyond that the user's password, hashed or not, should never need to be displayed.

This class is unused by this tutorial, but it is a template that can be used to easily retrieve information from a database table. When you're ready to move on beyond the login page, you can easily use PDO to fill class variables from corresponding variables in a database table with a call like _$stmt->setFetchMode(PDO::FETCH_CLASS, 'UserData')_, and then calling _$stmt->fetch(PDO::FETCH_CLASS)_ to fill the class variables.

```php
<?php

class UserData { public $UserID; public $Username; }

?>
```

**class-users.php**

The _Users_ class is used to retrieve, assess, and modify data stored in the _UserData_ class. For our purposes, we only need a _checkCredentials()_ function to validate the given _username_ and _password_ against MySQL database elements.

```php
<?php

require_once ('class-databasehelpers.php'); require_once ('class-userdata.php');

class Users { public function checkCredentials($username, $password) { // A UserID of 0 from the database indicates that the username/password pair // could not be found in the database $userID = 0; $digest = '';

try { $dbh = DatabaseHelpers::getDatabaseConnection();

// Build a prepared statement that looks for a row containing the given // username/password pair $stmt = $dbh->prepare('SELECT UserID, Password FROM Users WHERE ' . 'Username=:username ' . 'LIMIT 1');

$stmt->bindParam(':username', $username, PDO::PARAM_STR);

$success = $stmt->execute();

// If results were returned from executing the MySQL command, we // have found the user if ($success) { // Ensure provided password matches stored hash $userData = $stmt->fetch(); $digest = $userData['Password']; if (crypt ($password, $digest) == $digest) { $userID = $userData['UserID']; } }

$dbh = null; } catch (PDOException $e) { $userID = 0; $digest = ''; }

return array ($userID, $username, $digest); } }

?>
```

**pages.php**

This class acts as an enum of pages on your site.

```php
<?php

// To get around the fact that PHP won't allow you to declare // a const with an expression, define our constants outside // the Page class, then use these variables within the class define ('LOGIN', 'Login'); define ('INDEX', 'Index');

class Page { const LOGIN = LOGIN; const INDEX = INDEX; }

?>
```

**functions.php**

Here's where it gets fun. As you create more pages that should only be accessible to validated users, make sure you add them as an OR to the return of _isSecuredPage()_.

The _checkLoggedIn()_ function is our primary work house. This function checks to see if the current page requires validation. If the page requires validation and the user is not logged in, they are redirected to **login.php**. If a user has been logged in and visits the login page, they are redirected to the main page. If the user has been logged in, this function allows them to access secured pages. The _checkLoggedIn()_ function is also responsible for completing both the login and logout process, and on successful login it sets the proper session and cookie variables.

Take note of how the _secondDigest_ cookie parameter is being used. We need to store authentication information in the cookie so we can securely implement the "Remember me" functionality, but if all we store are credentials, the cookie could still be stolen and used. To prevent against this, we also store physical characteristics of the connection, in this case IP address and HTTP User Agent information. That data should be hashed as well so a hijacker can't just spoof it when they steal the cookie. Now, if a hijacker takes our cookie to their own computer, the cookie will pass user authentication but fail the second digest, and the hijacker will be prompted to login again.

You would be wise to modify what exactly is in the second digest. If a standard were used, hashing it would pointless, even with the salt. Additional salt beyond the Blowfish cypher would be good, adding additional information, reordering the information before it's hashed, etc. For increased security, you could also store the second digest on the server in the Users table, comparing the cookie's value with that value (which would need to be updated after each successful login).

```php
<?php

require_once ('class-databasehelpers.php'); require_once ('class-users.php'); require_once ('functions.php'); require_once ('pages.php');

function isSecuredPage($page) { // Return true if the given page should only be accessible to validation users return $page == Page::INDEX; }

function checkLoggedIn($page) { $loginDiv = ''; $action = ''; if (isset($_POST['action'])) { $action = stripslashes ($_POST['action']); }

session_start ();

// Check if we're already logged in, and check session information against cookies // credentials to protect against session hijacking if (isset ($_COOKIE['project-name']['userID']) && crypt($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT'], $_COOKIE['project-name']['secondDigest']) == $_COOKIE['project-name']['secondDigest'] && (!isset ($_COOKIE['project-name']['username']) || (isset ($_COOKIE['project-name']['username']) && Users::checkCredentials($_COOKIE['project-name']['username'], $_COOKIE['project-name']['digest'])))) { // Regenerate the ID to prevent session fixation session_regenerate_id ();

// Restore the session variables, if they don't exist if (!isset ($_SESSION['project-name']['userID'])) { $_SESSION['project-name']['userID'] = $_COOKIE['project-name']['userID']; }

// Only redirect us if we're not already on a secured page and are not // receiving a logout request if (!isSecuredPage ($page) && $action != 'logout') { header ('Location: ./');

exit; } } else { // If we're not already the login page, redirect us to the login page if ($page != Page::LOGIN) { header ('Location: login.php');

exit; } }

// If we're not already logged in, check if we're trying to login or logout if ($page == Page::LOGIN && $action != '') { switch ($action) { case 'login': { $userData = Users::checkCredentials (stripslashes ($_POST['login-username']), stripslashes ($_POST['password'])); if ($userData[0] != 0) { $_SESSION['project-name']['userID'] = $userData[0]; $_SESSION['project-name']['ip'] = $_SERVER['REMOTE_ADDR']; $_SESSION['project-name']['userAgent'] = $_SERVER['HTTP_USER_AGENT']; if (isset ($_POST['remember'])) { // We set a cookie if the user wants to remain logged in after the // browser is closed // This will leave the user logged in for 168 hours, or one week setcookie('project-name[userID]', $userData[0], time () + (3600 \* 168)); setcookie('project-name[username]', $userData[1], time () + (3600 \* 168)); setcookie('project-name[digest]', $userData[2], time () + (3600 \* 168)); setcookie('project-name[secondDigest]', DatabaseHelpers::blowfishCrypt($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT'], 10), time () + (3600 \* 168)); } else { setcookie('project-name[userID]', $userData[0], false); setcookie('project-name[username]', '', false); setcookie('project-name[digest]', '', false); setcookie('project-name[secondDigest]', DatabaseHelpers::blowfishCrypt($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT'], 10), time () + (3600 \* 168)); }

header ('Location: ./');

exit; } else { $loginDiv = ' <div id="login-box" class="error">The username or password ' .</div> <pre> 'you entered is incorrect.</div>'; } break; } // Destroy the session if we received a logout or don't know the action received case 'logout': default: { // Destroy all session and cookie variables $_SESSION = array (); setcookie('project-name[userID]', '', time () - (3600 \* 168)); setcookie('project-name[username]', '', time () - (3600 \* 168)); setcookie('project-name[digest]', '', time () - (3600 \* 168)); setcookie('project-name[secondDigest]', '', time () - (3600 \* 168));

// Destory the session session_destroy ();

$loginDiv = ' <div id="login-box" class="info">Thank you. Come again!</div> <pre>';

break; } } }

return $loginDiv; }

?>
```

**login.php**

This is the base for a login form on the login page. Notice that now we're modifying front-centric PHP files, the only reference you see to heavy lifting is a simple call to our _checkLoggedIn()_ function. The form handles POSTing to this page to log the user in and redirect them to **index.php**.

The _$loginDiv_ that we receive from _checkLoggedIn()_ allows us to display informative statuses to the user, for instance, if they try to login with the wrong password.

```php
<?php

require_once ('functions.php');

// Check to see if we're already logged in or if we have a special status div to report $loginDiv = checkLoggedIn (Page::LOGIN);

?>

<html> <body> <h2>Sign in</h2> <form name="login" method="post" action="login.php"> <input type="hidden" name="action" value="login" /> <label for="login-username">Username:</label><br /> <input id="login-username" name="login-username" type="text" /><br /> <label for="password">Password:</label><br /> <input name="password" type="password" /><br /> <input id="remember" name="remember" type="checkbox" /> <label for="remember">Remember me</label><br /> <!--?php echo $<span class="hiddenSpellError" pre="echo " data-mce-bogus="1"-->loginDiv ?> <input type="submit" value="Login" /> </form> </body> </html>
```

**index.php**

Last, but certainly not least, our secured pages. All the work we've done above to ensure a robust application allows us to make one simple call from a secured page: _checkLoggedIn()_. Everything we've done above handles the rest. Add this call to any page you want to be secured and you're good to go!

One thing to note is the logout button, which simple POSTs a logout action to **login.php**.

```php
<?php

require_once ('functions.php');

checkLoggedIn (Page::INDEX);

?>

<html> <body> <form name="logout" method="post" action="login.php"> <input type="hidden" name="action" value="logout" /> <input type="submit" value="Logout" /> </form> </body> </html>
```

# The Common Exit Issue

Take special note that as soon as it has been determined that _checkLoggedIn()_ in **functions.php** succeeded or failed (i.e. following a header call to redirect), exit has been called. This is crucial if your secured page makes ready use of your session or cookie variables, because it tells PHP to cease construction of the page immediately. It is a common mistake to not call exit after a header redirect, which is not necessarily insecure, but it is poor practice. If you fail to call exit immediately, the remainder of the page will still be evaluated by PHP (though the variables may not have been initialized), and error reports may occur. Not data will be displayed to the user, but you neglecting to call exit may fill up your PHP error logs.

# The Payoff

You now have login page, secured content areas, cookie storage for returning users, and working sessions throughout your pages. What's cool about this from this point forward is that you can easily apply this new knowledge of cookies and sessions outside of the credentials realm.

You now have live sessions on your pages, so you can store additional values in the $_SESSION variable to carry them between pages. You've seen how cookies work, so you can curse your clients with crumbles of your website for the next time they return (don't be evil).

If you have any further questions regarding the login process, sessions, or cookies, or if you just found this tutorial useful, let me know in a comment.
