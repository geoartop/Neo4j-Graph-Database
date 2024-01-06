//2. Count all users, count all targets, count all actions:
MATCH (u:User)
RETURN count (u)

MATCH (t:Target)
RETURN count (t)

MATCH (u:User)-[a:ACTION]->(t:Target)
RETURN count(a)

//3. Show all actions (actionID) and targets (targetID) of a specific user (choose one):
MATCH (u:User {user_id: 3})-[a:ACTION]->(t:Target)
RETURN a.action_id, t.target_id

//4. For each user, count his/her actions:
MATCH (u:User)-[a:ACTION]->(t:Target)
RETURN u.user_id, count (a)

//5. For each target, count how many users have done this target:
MATCH (u:User)-[a:ACTION]->(t:Target)
RETURN t.target_id, count(DISTINCT u)

//6. Count the average actions per user:
MATCH (u:User)-[a:ACTION]->(t:Target)
WITH count(a) AS totalActions, count (DISTINCT u) AS totalUsers
RETURN totalActions / totalUsers AS averageActionsPerUser

//7. Show the userID and the targetID, if the action has positive Feature2:
MATCH (u:User)-[a:ACTION]->(t:Target)
  WHERE a.action_feature2 > 0
RETURN u.user_id, t.target_id

//8. For each targetID, count the actions with label “1”:
MATCH (u:User)-[a:ACTION {action_label: 1}]->
(t:Target)
RETURN t.target_id, count(a)
  ORDER BY t.target_id
