from models.applications import ApplicationsModel
from models.jobs import JobsModel
from models.favorites import FavoritesModel

class Helper():

    def del_applications_by_job(job_id):
        for app in ApplicationsModel.find_by_job_id(job_id):
            app.delete_from_db()
        return

    def del_applications_by_user(user_id):
        for app in ApplicationsModel.find_by_user_id(user_id):
            app.delete_from_db()
        return

    def del_applications_by_company(company_id):
        for app in ApplicationsModel.find_by_company_id(company_id):
            app.delete_from_db()
        return

    def del_jobs_by_company(company_id):
        for job in JobsModel.find_by_company_id(company_id):
            job.delete_from_db()
        return

    def del_favorites_by_user(user_id):
        for favorite in FavoritesModel.find_by_user_id(user_id):
            favorite.delete_from_db()
        return

    def del_favorites_by_company(company_id):
        for app in FavoritesModel.find_by_company_id(company_id):
            app.delete_from_db()
        return

    def del_favorites_by_job(job_id):
        for favorite in FavoritesModel.find_by_job_id(job_id):
            favorite.delete_from_db()
        return