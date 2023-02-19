from django.urls import path
from .views import CompanieView,CreateCompanieView,FilterCompanieView,GetCompanieInfo,CompanyFirstChartData,CompanyOtherChartData,UpdateSessionTimePeriode,NextEarningsView

urlpatterns = [
    path('', CompanieView.as_view(),name='companielist'),
    path('add',CreateCompanieView.as_view()),
    path('filterCompany/',FilterCompanieView.as_view()),
    path('get-company-info',GetCompanieInfo.as_view()),
    path('get-first-company-chart',CompanyFirstChartData.as_view()),
    path('get-other-company-chart',CompanyOtherChartData.as_view()),
    path('update-session-time-periode',UpdateSessionTimePeriode.as_view()),
    path('next-earnings',NextEarningsView.as_view()),
]