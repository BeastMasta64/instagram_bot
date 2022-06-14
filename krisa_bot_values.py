element_for_size_xpath = {
    'followers': '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]/ul',
    'followings': '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/ul',
}

# element_for_size_xpath = {
#     'followers': '/html/body/div[6]/div/div/div/div[2]/ul',
#     'followings': '/html/body/div[6]/div/div/div/div[3]/ul',
# }
element_to_scroll_xpath = {
    'followers': '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]',
    'followings': '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]'
}

# element_to_scroll_xpath = {
#     'followers': '/html/body/div[6]/div/div/div/div[2]',
#     'followings': '/html/body/div[6]/div/div/div/div[3]'
# }


users_xpath = {
    'followers': '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]/ul/div/li',
    'followings': '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/ul/div/li'
}
# users_xpath = {
#     'followers': '/html/body/div[6]/div/div/div/div[2]/ul/div/li',
#     'followings': '/html/body/div[6]/div/div/div/div[3]/ul/div/li'
# }
username_element_xpath_list = ['./div/div[2]/div[1]/div/div/span/a/span', './div/div[1]/div[2]/div[1]/span/a/span']
users_button_xpath = {
    'followers': '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div',
    'followings': '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div',
}
# users_button_xpath = {
#     'followers': '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div',
#     'followings': '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/div',
# }

users_quantity_xpath = {
    'followers': '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span',
    'followings': '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div/span'
}
# users_quantity_xpath = {
#     'followers': '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span',
#     'followings': '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/div/span'
# }
