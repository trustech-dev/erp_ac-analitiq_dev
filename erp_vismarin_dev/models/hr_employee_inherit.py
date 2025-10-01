from odoo import models, fields


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    project_count = fields.Integer(compute="compute_count_project")

    def compute_count_project(self):
        if self.user_id:
            tasks = self.env["project.task"].search(
                [("allowed_user_ids", "in", self.user_id.id)]
            )
            project_list = set()
            for task in tasks:
                project_list.add(task.project_id.id)
            self.project_count = len(project_list)
        else:
            self.project_count = 0

    def get_project_list(self):
        print("user:", self.user_id.id)
        tasks = self.env["project.task"].search(
            [("allowed_user_ids", "in", self.user_id.id)]
        )
        project_list = set()
        for task in tasks:
            project_list.add(task.project_id.id)

        if len(project_list) > 0:
            tasks = self.env["project.task"].search(
                [("allowed_user_ids", "in", self.user_id.id)]
            )
            project_list = set()
            for task in tasks:
                project_list.add(task.project_id.id)

            action = self.env.ref("project.open_view_project_all").read()[0]
            action["domain"] = [("id", "in", list(project_list))]
            return action
        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "type": "warning",
                    "message": "There is no project ",
                    "sticky": False,
                },
            }
