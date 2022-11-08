create database Zomato;

use Zomato;

select * from zomato_1_cleand;




-- area wise distribution of restaurant

--- Based on total no number of restaurant in bangaulore mention in zomato 

select location , count_of_restaurant from distribution_of_restaurant_ order by count_of_restaurant desc;

-- Which location have maximum  number of restaurant  top two.

select top 2 location , count_of_restaurant from distribution_of_restaurant_ order by count_of_restaurant desc ;

-- Which location have minimum number of restaurant where the delivery_review_number is greater than 1000. top two.

select top 2 location , count_of_restaurant from distribution_of_restaurant_ order by count_of_restaurant asc ;

-----now out of all the restaurant we took the data 1055 restaurant randomly from every locations-----


---Which location have minimum number of restaurant where the delivery_review_number is greater than 1000.

select top 14 location,count(Name) as restaurant_count from zomato_1_cleand where delivery_review_number>1000
group by location order by restaurant_count desc

--- Which location maximum number of less rated restaurant.

--took locations where restaurant is more than 10 in number.

select top 10 location , count(name) as no_of_restaurants  , avg(Rating) average_rating 
from zomato_1_cleand group by location 
having count(name) > 9
order by avg(Rating);

-- Which location maximum number of less rated restaurant.
select top 10 location , count(name) as no_of_restaurants  , avg(Rating) average_rating 
from zomato_1_cleand group by location 
having count(name) > 9
order by avg(Rating) desc ;

--- Area wise cheap and expensive restaurant and their average price

--avg_price cheap reastuarant


select  top 5 restaurant_name   , avg(dish_price) as avg_price 
from zomato_2_cleand 
group by restaurant_name
order by avg(dish_price) ;

--avg_price expensive reastuarant


select  top 5 restaurant_name , avg(dish_price) as  avg_price 
from zomato_2_cleand 
group by restaurant_name
order by avg(dish_price) desc ;


--Number of restaurant for each type of cuisine. 

select top 10 count(Name) as No_restaurant,cusines from zomato_1_cleand group by cusines
order by count(Name) desc

--cheapest cusine
select *,DENSE_RANK() over (partition by Restaurant_Name order by Dish_Price) as price_Rank from  zomato_2_cleand 

select top 2 a.Restaurant_Name,a.Dish_Name,a.Dish_Price from
(select *,DENSE_RANK() over (partition by Restaurant_Name order by Dish_Price)
as price_Rank from  zomato_2_cleand) as a
where price_Rank=1




