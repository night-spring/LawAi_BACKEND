from django.db import models

class Query(models.Model):
    """
    Stores user queries and responses.
    """
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query: {self.query[:50]}..."  # Display first 50 characters


class BNS(models.Model):
    section_id = models.TextField()
    section_title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"BNS: {self.section_id} - {self.section_title} -> {self.description}..."

class IPC(models.Model):
    section_id = models.TextField()
    section_title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"IPC: {self.section_id} - {self.section_title} -> {self.description}..."

class CrPC(models.Model):
    section_id = models.TextField()
    section_title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"IPC: {self.section_id} - {self.section_title} -> {self.description}..."

class MVA(models.Model):
    section_id = models.TextField()
    section_title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"IPC: {self.section_id} - {self.section_title} -> {self.description}..."

class CPC(models.Model):
    section_id = models.TextField()
    section_title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"IPC: {self.section_id} - {self.section_title} -> {self.description}..."

class IEA(models.Model):
    section_id = models.TextField()
    section_title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f"IPC: {self.section_id} - {self.section_title} -> {self.description}..."

class Document(models.Model):
    act_name = models.TextField()
    description = models.TextField()
    pdf = models.BinaryField()  # Store the binary data of the PDF

    def __str__(self):
        return self.act_name

class Case(models.Model):
    caseHeading = models.TextField()
    applicableArticle = models.TextField()
    tags = models.TextField()
    query = models.TextField()
    status = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.caseHeading

