from django.urls import reverse

def tree_items(request):
    tree_data = [
        {
            "name": "Home",
            "url": reverse("home"),
            "type": "folder",
            "children": [
                {
                    "name": "About",
                    "url": "#",
                    "type": "file"
                },
                {
                    "name": "Contact",
                    "url": "#",
                    "type": "file"
                }
            ]
        },
        {
            "name": "Financial Overview",
            "url": "#",
            "type": "folder",
            "children": [
                {
                    "name": "Outgoings Table",
                    "url": "#",
                    "type": "file"
                },
                {
                    "name": "Savings Table",
                    "url": "#",
                    "type": "file"
                },
                {
                    "name": "Budget Table",
                    "url": "#",
                    "type": "file"
                }
            ]
        },
        {
            "name": "Dashboards",
            "url": "#",
            "type": "folder",
            "children": [
                {
                    "name": "Outgoings Dashboard",
                    "url": "#",
                    "type": "file"
                },
                {
                    "name": "Savings Dashboard",
                    "url": "#",
                    "type": "file"
                },
                {
                    "name": "Budget Dashboard",
                    "url": "#",
                    "type": "file"
                }
            ]
        }
    ]
    
    return {'tree_items': tree_data}