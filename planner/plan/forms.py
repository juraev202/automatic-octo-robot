from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


from .models import Plan, Category
class RegForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PlanForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Choose Existing Category"
    )
    new_category = forms.CharField(
        required=False,
        label="Or Add New Category",
        help_text="Leave empty if using the dropdown above."
    )
    reminder_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Remind Me At"
    )

    class Meta:
        model = Plan
        fields = ['title', 'description', 'photo', 'category', 'new_category', 'reminder_time']

    def save(self, commit=True):
        instance = super().save(commit=False)

        new_cat = self.cleaned_data.get('new_category')
        existing_cat = self.cleaned_data.get('category')

        # Determine which category to use
        if new_cat:
            category, _ = Category.objects.get_or_create(category_name=new_cat)
            instance.plan_category = category
        elif existing_cat:
            instance.plan_category = existing_cat
        else:
            raise forms.ValidationError("You must select or enter a category.")

        if commit:
            instance.save()

        return instance
