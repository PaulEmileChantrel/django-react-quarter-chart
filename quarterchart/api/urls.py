from django.urls import path
from .views import CompanieView,CreateCompanieView,FilterCompanieView,GetCompanieInfo,CompanyFirstChartData,CompanyOtherChartData,UpdateSessionTimePeriode,NextEarningsView

urlpatterns = [
    path('', CompanieView.as_view(),name='companielist'),
    path('add',CreateCompanieView.as_view(),name='create_companie'),
    path('filterCompany/',FilterCompanieView.as_view(),name='filter-companies'),
    path('get-company-info',GetCompanieInfo.as_view(),name='get-companie-info'),
    path('get-first-company-chart',CompanyFirstChartData.as_view(),name='company_first_chart_data'),
    path('get-other-company-chart',CompanyOtherChartData.as_view(),name='company_other_chart_data'),
    path('update-session-time-periode',UpdateSessionTimePeriode.as_view(),name='update_session_time_periode'),
    path('next-earnings',NextEarningsView.as_view()),
]