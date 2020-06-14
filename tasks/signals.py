from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from tasks.models import TodoItem, Category, Priority
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "post_add":
        return

    for cat in instance.category.all():
        slug = cat.slug

        new_count = 0
        for task in TodoItem.objects.all():
            new_count += task.category.filter(slug=slug).count()

        Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    cat_counter = Counter()
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            cat_counter[cat.slug] += 1

    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)

@receiver(m2m_changed, sender=TodoItem.priority.through)
def task_priority_added(sender, instance, action, model, **kwargs):
    if action != "post_add":
        return

    for prior in instance.priority.all():
        slug = prior.slug

        new_count = 0
        for task in TodoItem.objects.all():
            new_count += task.priority.filter(slug=slug).count()

        Priority.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.priority.through)
def task_priority_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    prior_counter = Counter()
    for t in TodoItem.objects.all():
        for prior in t.priority.all():
            prior_counter[prior.slug] += 1

    for slug, new_count in prior_counter.items():
        Priority.objects.filter(slug=slug).update(todos_count=new_count)