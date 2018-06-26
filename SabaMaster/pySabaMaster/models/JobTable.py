from pySabaMaster.models import db
from datetime import datetime


class JobTable(db.Model):
    __tablename__ = 'job_table'

    job_id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(127), nullable=True)
    SRA_accession_nums = db.Column(db.Text)
    CWL_filepaths = db.Column(db.Text)
    output_base_path = db.Column(db.String(127))
    status = db.Column(db.String(31))
    instance_size = db.Column(db.String(31))
    disk_size = db.Column(db.String(31))
    log_path = db.Column(db.String(127))
    start_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    finish_timestamp = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(JobTable, self).__init__(**kwargs)

    def __repr__(self):
        return '<Job_ID %r>' % self.job_id

    def as_dict(self):
        if self.finish_timestamp is None:
            self.finish_timestamp = ""
        _dict = {"job_id": int(self.job_id),
                 "job_name": str(self.job_name),
                 "SRA_accession_nums": list(map(str, self.SRA_accession_nums.split(","))),
                 "CWL_filepaths": list(map(str, self.SRA_accession_nums.split(","))),
                 "output_base_path": str(self.output_base_path),
                 "status": str(self.status),
                 "instance_size": str(self.instance_size),
                 "disk_size": str(self.disk_size),
                 "log_path": str(self.log_path),
                 "start_timestamp": str(self.start_timestamp),
                 "finish_timestamp": str(self.finish_timestamp)
                 }

        return _dict
